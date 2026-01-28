"""
Machine Learning Models for Healthcare Analytics
- Readmission Prediction (30-day readmission risk)
- Risk Scoring (overall health risk 0-100)
- Disease Progression Prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score
from imblearn.over_sampling import SMOTE
import joblib
import os
from datetime import datetime

class HealthcareMLModels:
    def __init__(self):
        self.readmission_model = None
        self.risk_model = None
        self.disease_progression_model = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.model_dir = 'ml_models_saved'
        
        # Create directory for saving models
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
    
    def prepare_readmission_data(self, patients_df, visits_df):
        """
        Prepare data for 30-day readmission prediction
        Target: readmitted_within_30_days (from visits)
        """
        # Merge patients and visits data
        merged = visits_df.merge(patients_df, on='patient_id', how='left')
        
        # Select relevant features from available fields
        feature_cols = [
            'age', 'gender', 'bmi', 'smoker_status', 'alcohol_use',
            'severity_score', 'length_of_stay', 'previous_visit_gap_days',
            'number_of_previous_visits'
        ]
        
        # Handle missing values
        for col in feature_cols:
            if col in merged.columns:
                if merged[col].dtype == 'object':
                    merged[col].fillna('Unknown', inplace=True)
                else:
                    merged[col].fillna(merged[col].median(), inplace=True)
        
        # Encode categorical variables
        categorical_cols = ['gender', 'smoker_status', 'alcohol_use']
        for col in categorical_cols:
            if col in merged.columns and col not in self.label_encoders:
                le = LabelEncoder()
                merged[col] = le.fit_transform(merged[col].astype(str))
                self.label_encoders[col] = le
            elif col in merged.columns:
                merged[col] = self.label_encoders[col].transform(merged[col].astype(str))
        
        # Extract features and target
        X = merged[feature_cols].copy()
        
        # Target variable - readmission within 30 days
        if 'readmitted_within_30_days' in merged.columns:
            y = merged['readmitted_within_30_days'].map({'Yes': 1, 'No': 0, 'yes': 1, 'no': 0, True: 1, False: 0})
            y = y.fillna(0).astype(int)
        else:
            # If not available, create synthetic target based on severity and length of stay
            y = ((merged['severity_score'] > 7) & (merged['length_of_stay'] > 5)).astype(int)
        
        return X, y
    
    def train_readmission_model(self, X, y):
        """
        Train Random Forest Classifier for 30-day readmission prediction
        """
        print("🧠 Training Readmission Prediction Model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Handle imbalanced data with SMOTE
        try:
            smote = SMOTE(random_state=42)
            X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
        except:
            X_train_balanced, y_train_balanced = X_train_scaled, y_train
        
        # Train model
        self.readmission_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.readmission_model.fit(X_train_balanced, y_train_balanced)
        
        # Evaluate
        y_pred = self.readmission_model.predict(X_test_scaled)
        y_pred_proba = self.readmission_model.predict_proba(X_test_scaled)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        try:
            auc = roc_auc_score(y_test, y_pred_proba)
            print(f"✅ Readmission Model - Accuracy: {accuracy:.2%}, AUC-ROC: {auc:.3f}")
        except:
            print(f"✅ Readmission Model - Accuracy: {accuracy:.2%}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.readmission_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("📊 Top 5 Features for Readmission:")
        print(feature_importance.head().to_string(index=False))
        
        return accuracy
    
    def prepare_risk_score_data(self, patients_df, visits_df):
        """
        Prepare data for health risk scoring (0-100 scale)
        Target: Composite risk score based on severity, chronic conditions, vitals
        """
        # Merge data
        merged = visits_df.merge(patients_df, on='patient_id', how='left')
        
        # Feature engineering - use available fields
        feature_cols = [
            'age', 'gender', 'bmi', 'smoker_status', 'alcohol_use',
            'severity_score', 'length_of_stay', 'number_of_previous_visits'
        ]
        
        # Handle missing values
        for col in feature_cols:
            if col in merged.columns:
                if merged[col].dtype == 'object':
                    merged[col].fillna('Unknown', inplace=True)
                else:
                    merged[col].fillna(merged[col].median(), inplace=True)
        
        # Encode categorical
        categorical_cols = ['gender', 'smoker_status', 'alcohol_use']
        for col in categorical_cols:
            if col in merged.columns and col not in self.label_encoders:
                le = LabelEncoder()
                merged[col] = le.fit_transform(merged[col].astype(str))
                self.label_encoders[col] = le
            elif col in merged.columns:
                merged[col] = self.label_encoders[col].transform(merged[col].astype(str))
        
        X = merged[feature_cols].copy()
        
        # Create composite risk score (target variable)
        # Risk = weighted combination of severity, age, lifestyle
        age_risk = np.clip((merged['age'] - 30) / 50 * 30, 0, 30)  # Max 30 points
        severity_risk = merged['severity_score'] * 5  # Max 50 points (severity 0-10)
        
        # Lifestyle risk
        lifestyle_risk = (merged['smoker_status'].map({1: 10, 0: 0}).fillna(0) +
                         merged['alcohol_use'].map({1: 5, 0: 0}).fillna(0))
        
        # Previous visits risk (more visits = higher risk)
        visit_risk = np.clip(merged['number_of_previous_visits'] * 2, 0, 15)
        
        y = np.clip(
            age_risk + severity_risk + lifestyle_risk + visit_risk,
            0, 100
        )
        
        return X, y
    
    def train_risk_scoring_model(self, X, y):
        """
        Train Gradient Boosting Regressor for health risk scoring
        """
        print("\n🧠 Training Risk Scoring Model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.risk_model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.risk_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.risk_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"✅ Risk Scoring Model - MSE: {mse:.2f}, R²: {r2:.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.risk_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("📊 Top 5 Features for Risk Scoring:")
        print(feature_importance.head().to_string(index=False))
        
        return r2
    
    def prepare_disease_progression_data(self, visits_df):
        """
        Prepare data for disease progression prediction
        Predict severity trend (improving/stable/worsening)
        """
        # Sort by patient and visit date
        visits_sorted = visits_df.sort_values(['patient_id', 'visit_date'])
        
        # Calculate severity change from previous visit
        visits_sorted['prev_severity'] = visits_sorted.groupby('patient_id')['severity_score'].shift(1)
        visits_sorted['severity_change'] = visits_sorted['severity_score'] - visits_sorted['prev_severity']
        
        # Remove first visits (no previous data)
        visits_sorted = visits_sorted.dropna(subset=['prev_severity'])
        
        # Features - use available fields
        feature_cols = [
            'prev_severity', 'length_of_stay', 'previous_visit_gap_days',
            'number_of_previous_visits'
        ]
        
        # Handle missing values
        for col in feature_cols:
            if col in visits_sorted.columns:
                visits_sorted[col].fillna(visits_sorted[col].median(), inplace=True)
        
        X = visits_sorted[feature_cols].copy()
        
        # Target: Progression category (0=Improving, 1=Stable, 2=Worsening)
        y = pd.cut(
            visits_sorted['severity_change'],
            bins=[-np.inf, -1, 1, np.inf],
            labels=[0, 1, 2]  # Improving, Stable, Worsening
        ).astype(int)
        
        return X, y
    
    def train_disease_progression_model(self, X, y):
        """
        Train Random Forest for disease progression prediction
        """
        print("\n🧠 Training Disease Progression Model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.disease_progression_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42,
            class_weight='balanced'
        )
        self.disease_progression_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.disease_progression_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Disease Progression Model - Accuracy: {accuracy:.2%}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.disease_progression_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("📊 Top 5 Features for Disease Progression:")
        print(feature_importance.head().to_string(index=False))
        
        return accuracy
    
    def save_models(self):
        """Save all trained models"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.readmission_model is not None:
            try:
                joblib.dump(
                    self.readmission_model,
                    f"{self.model_dir}/readmission_model_{timestamp}.pkl"
                )
                print(f"✅ Saved readmission model")
            except:
                pass
        
        if self.risk_model is not None:
            try:
                joblib.dump(
                    self.risk_model,
                    f"{self.model_dir}/risk_model_{timestamp}.pkl"
                )
                print(f"✅ Saved risk scoring model")
            except:
                pass
        
        if self.disease_progression_model is not None:
            try:
                joblib.dump(
                    self.disease_progression_model,
                    f"{self.model_dir}/disease_progression_model_{timestamp}.pkl"
                )
                print(f"✅ Saved disease progression model")
            except:
                pass
        
        # Save encoders and scaler
        try:
            joblib.dump(self.label_encoders, f"{self.model_dir}/label_encoders_{timestamp}.pkl")
            joblib.dump(self.scaler, f"{self.model_dir}/scaler_{timestamp}.pkl")
            print(f"✅ Saved encoders and scaler")
        except:
            pass
    
    def load_models(self, timestamp=None):
        """Load saved models"""
        if timestamp is None:
            # Find latest models
            files = os.listdir(self.model_dir)
            # Extract full timestamp from filenames like "readmission_model_20260119_054913.pkl"
            timestamps = []
            for f in files:
                if 'readmission_model_' in f and f.endswith('.pkl'):
                    # Extract timestamp part after "readmission_model_"
                    ts = f.replace('readmission_model_', '').replace('.pkl', '')
                    timestamps.append(ts)
            
            if timestamps:
                timestamp = sorted(timestamps)[-1]
        
        if timestamp:
            try:
                self.readmission_model = joblib.load(
                    f"{self.model_dir}/readmission_model_{timestamp}.pkl"
                )
                self.risk_model = joblib.load(
                    f"{self.model_dir}/risk_model_{timestamp}.pkl"
                )
                self.disease_progression_model = joblib.load(
                    f"{self.model_dir}/disease_progression_model_{timestamp}.pkl"
                )
                self.label_encoders = joblib.load(
                    f"{self.model_dir}/label_encoders_{timestamp}.pkl"
                )
                self.scaler = joblib.load(
                    f"{self.model_dir}/scaler_{timestamp}.pkl"
                )
                print(f"✅ Loaded models from {timestamp}")
                return True
            except Exception as e:
                print(f"❌ Error loading models: {e}")
                return False
        return False
    
    def predict_readmission(self, patient_data):
        """
        Predict 30-day readmission probability
        
        Args:
            patient_data: dict with keys matching feature columns
        
        Returns:
            dict with prediction and probability
        """
        if not self.readmission_model:
            return {"error": "Model not trained yet"}
        
        # Prepare input
        X = pd.DataFrame([patient_data])
        
        # Encode categorical
        categorical_cols = ['gender', 'smoker_status', 'alcohol_use']
        for col in categorical_cols:
            if col in X.columns and col in self.label_encoders:
                X[col] = self.label_encoders[col].transform(X[col].astype(str))
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.readmission_model.predict(X_scaled)[0]
        probability = self.readmission_model.predict_proba(X_scaled)[0]
        
        return {
            "readmission_risk": "High" if prediction == 1 else "Low",
            "probability": float(probability[1]),
            "recommendation": "Close monitoring required" if prediction == 1 else "Standard care protocol"
        }
    
    def predict_risk_score(self, patient_data):
        """
        Predict overall health risk score (0-100)
        
        Args:
            patient_data: dict with keys matching feature columns
        
        Returns:
            dict with risk score and category
        """
        if not self.risk_model:
            return {"error": "Model not trained yet"}
        
        # Prepare input
        X = pd.DataFrame([patient_data])
        
        # Encode categorical
        categorical_cols = ['gender', 'smoker_status', 'alcohol_use']
        for col in categorical_cols:
            if col in X.columns and col in self.label_encoders:
                X[col] = self.label_encoders[col].transform(X[col].astype(str))
        
        # Predict
        risk_score = self.risk_model.predict(X)[0]
        risk_score = np.clip(risk_score, 0, 100)
        
        # Categorize risk
        if risk_score < 30:
            category = "Low Risk"
            color = "green"
        elif risk_score < 60:
            category = "Moderate Risk"
            color = "yellow"
        else:
            category = "High Risk"
            color = "red"
        
        return {
            "risk_score": float(risk_score),
            "category": category,
            "color": color
        }
    
    def predict_disease_progression(self, visit_data):
        """
        Predict disease progression trend
        
        Args:
            visit_data: dict with current visit metrics
        
        Returns:
            dict with progression prediction
        """
        if not self.disease_progression_model:
            return {"error": "Model not trained yet"}
        
        # Prepare input
        X = pd.DataFrame([visit_data])
        
        # Predict
        prediction = self.disease_progression_model.predict(X)[0]
        probability = self.disease_progression_model.predict_proba(X)[0]
        
        progression_map = {
            0: "Improving",
            1: "Stable",
            2: "Worsening"
        }
        
        return {
            "progression": progression_map[prediction],
            "confidence": float(max(probability)),
            "probabilities": {
                "improving": float(probability[0]),
                "stable": float(probability[1]),
                "worsening": float(probability[2])
            }
        }
