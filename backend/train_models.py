"""
Train Machine Learning Models using MongoDB data
Run this script to train all three ML models with your 12,000+ patient records
"""

import pandas as pd
import numpy as np
from pymongo import MongoClient
from ml_models import HealthcareMLModels
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'healthcare_analytics')

print("="*60)
print("🏥 Healthcare ML Model Training Pipeline")
print("="*60)

# Connect to MongoDB
print("\n📊 Connecting to MongoDB...")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# Load data from MongoDB
print("📥 Loading patient data from MongoDB...")
patients_cursor = db.patients_processed.find()
patients_df = pd.DataFrame(list(patients_cursor))
print(f"✅ Loaded {len(patients_df)} patient records")

print("📥 Loading visit data from MongoDB...")
visits_cursor = db.visits_processed.find()
visits_df = pd.DataFrame(list(visits_cursor))
print(f"✅ Loaded {len(visits_df)} visit records")

# Generate synthetic visit data if needed
if len(visits_df) < 100 and len(patients_df) > 100:
    print("\n🔧 Generating synthetic visit data from patient records...")
    
    # Create synthetic visits based on patient data
    synthetic_visits = []
    np.random.seed(42)
    
    for _, patient in patients_df.head(1000).iterrows():  # Use first 1000 patients
        # Generate 1-3 visits per patient
        num_visits = np.random.randint(1, 4)
        
        for i in range(num_visits):
            visit = {
                'visit_id': f"{patient['patient_id']}_V{i+1}",
                'patient_id': patient['patient_id'],
                'visit_date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 365)),
                'severity_score': np.random.randint(1, 11),
                'length_of_stay': np.random.randint(1, 15),
                'previous_visit_gap_days': np.random.randint(7, 180) if i > 0 else 0,
                'number_of_previous_visits': i,
                'readmitted_within_30_days': np.random.choice([0, 1], p=[0.7, 0.3])
            }
            synthetic_visits.append(visit)
    
    visits_df = pd.DataFrame(synthetic_visits)
    print(f"✅ Generated {len(visits_df)} synthetic visit records")

# Check if we have enough data
if len(patients_df) < 100:
    print("⚠️  Warning: Insufficient patient data. Need at least 100 records.")
    print("   Please run PySpark processor to load more data.")
    exit(1)

# Merge patient data with visits for training
print("\n🔧 Preparing training dataset...")
merged_df = visits_df.merge(patients_df, on='patient_id', how='left')
print(f"✅ Merged dataset: {len(merged_df)} records")

# Initialize ML models
print("\n🔧 Initializing ML models...")
ml_models = HealthcareMLModels()

# Train Model 1: Readmission Prediction
print("\n" + "="*60)
print("MODEL 1: 30-DAY READMISSION PREDICTION")
print("="*60)
try:
    X_readmission, y_readmission = ml_models.prepare_readmission_data(patients_df, visits_df)
    print(f"📊 Training data shape: {X_readmission.shape}")
    print(f"📊 Target distribution: {y_readmission.value_counts().to_dict()}")
    
    accuracy_readmission = ml_models.train_readmission_model(X_readmission, y_readmission)
    print(f"🎯 Final Accuracy: {accuracy_readmission:.2%}")
except Exception as e:
    print(f"❌ Error training readmission model: {e}")

# Train Model 2: Risk Scoring
print("\n" + "="*60)
print("MODEL 2: HEALTH RISK SCORING (0-100)")
print("="*60)
try:
    X_risk, y_risk = ml_models.prepare_risk_score_data(patients_df, visits_df)
    print(f"📊 Training data shape: {X_risk.shape}")
    print(f"📊 Risk score range: {y_risk.min():.2f} - {y_risk.max():.2f}")
    
    r2_risk = ml_models.train_risk_scoring_model(X_risk, y_risk)
    print(f"🎯 Final R² Score: {r2_risk:.3f}")
except Exception as e:
    print(f"❌ Error training risk scoring model: {e}")

# Train Model 3: Disease Progression
print("\n" + "="*60)
print("MODEL 3: DISEASE PROGRESSION PREDICTION")
print("="*60)
try:
    if len(visits_df) > 20:  # Need sufficient visit history
        X_progression, y_progression = ml_models.prepare_disease_progression_data(visits_df)
        print(f"📊 Training data shape: {X_progression.shape}")
        print(f"📊 Progression distribution: {y_progression.value_counts().to_dict()}")
        
        accuracy_progression = ml_models.train_disease_progression_model(X_progression, y_progression)
        print(f"🎯 Final Accuracy: {accuracy_progression:.2%}")
    else:
        print("⚠️  Insufficient visit history for disease progression model")
except Exception as e:
    print(f"❌ Error training disease progression model: {e}")

# Save all models
print("\n" + "="*60)
print("💾 SAVING TRAINED MODELS")
print("="*60)
ml_models.save_models()

# Test predictions with sample data
print("\n" + "="*60)
print("🧪 TESTING PREDICTIONS WITH SAMPLE DATA")
print("="*60)

# Sample patient for testing (use values matching the actual data format)
sample_patient_readmission = {
    'age': 65,
    'gender': 'Male',
    'bmi': 28.5,
    'smoker_status': 'yes',
    'alcohol_use': 'no',
    'severity_score': 7,
    'length_of_stay': 4,
    'previous_visit_gap_days': 45,
    'number_of_previous_visits': 3
}

sample_patient_risk = {
    'age': 65,
    'gender': 'Male',
    'bmi': 28.5,
    'smoker_status': 'yes',
    'alcohol_use': 'no',
    'severity_score': 7,
    'length_of_stay': 4,
    'number_of_previous_visits': 3
}

print("\n📋 Sample Patient Profile:")
for key, value in sample_patient_readmission.items():
    print(f"   {key}: {value}")

# Test readmission prediction
print("\n🔮 Readmission Prediction:")
readmission_result = ml_models.predict_readmission(sample_patient_readmission)
print(f"   Risk Level: {readmission_result.get('readmission_risk', 'N/A')}")
print(f"   Probability: {readmission_result.get('probability', 0):.1%}")
print(f"   Recommendation: {readmission_result.get('recommendation', 'N/A')}")

# Test risk scoring
print("\n🔮 Health Risk Score:")
risk_result = ml_models.predict_risk_score(sample_patient_risk)
print(f"   Risk Score: {risk_result.get('risk_score', 0):.1f}/100")
print(f"   Category: {risk_result.get('category', 'N/A')}")

# Test disease progression
print("\n🔮 Disease Progression:")
sample_visit = {
    'prev_severity': 5,
    'length_of_stay': 4,
    'previous_visit_gap_days': 45,
    'number_of_previous_visits': 3
}
progression_result = ml_models.predict_disease_progression(sample_visit)
print(f"   Trend: {progression_result.get('progression', 'N/A')}")
print(f"   Confidence: {progression_result.get('confidence', 0):.1%}")

print("\n" + "="*60)
print("✅ MODEL TRAINING COMPLETE!")
print("="*60)
print("\n📝 Next Steps:")
print("   1. Models saved in 'ml_models_saved/' directory")
print("   2. Use app.py API endpoints for real-time predictions")
print("   3. Integrate predictions into frontend dashboard")
print("   4. Monitor model performance over time")

client.close()
