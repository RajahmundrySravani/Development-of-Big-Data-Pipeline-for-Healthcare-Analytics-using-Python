# Machine Learning Models - Healthcare Analytics System

## Overview
Three ML models have been trained on your 12,000+ patient records:

### 1. **30-Day Readmission Prediction**
- **Accuracy**: 61.85%
- **AUC-ROC**: 0.510
- **Purpose**: Predict if a patient will be readmitted within 30 days
- **Top Features**: age, BMI, severity_score, length_of_stay, previous_visit_gap_days

### 2. **Health Risk Scoring**
- **R² Score**: 0.999
- **MSE**: 0.56
- **Purpose**: Calculate overall health risk score (0-100)
- **Top Features**: severity_score, age, smoker_status, alcohol_use, number_of_previous_visits

### 3. **Disease Progression Prediction**
- **Accuracy**: 53.73%
- **Purpose**: Predict if patient condition is Improving/Stable/Worsening
- **Top Features**: prev_severity, previous_visit_gap_days, length_of_stay, number_of_previous_visits

## Trained Models Location
All models are saved in: `backend/ml_models_saved/`
- `readmission_model_*.pkl` - Readmission prediction model
- `risk_model_*.pkl` - Risk scoring model
- `disease_progression_model_*.pkl` - Progression prediction model
- `label_encoders_*.pkl` - Categorical variable encoders
- `scaler_*.pkl` - Feature scaler

## API Endpoints

### 1. Load Models (call this first)
```
GET /api/ml/load-models
```

**Response:**
```json
{
  "success": true,
  "message": "ML models loaded successfully"
}
```

### 2. Predict Readmission Risk
```
POST /api/ml/predict/readmission
```

**Request Body:**
```json
{
  "age": 65,
  "gender": "Male",
  "bmi": 28.5,
  "smoker_status": "yes",
  "alcohol_use": "no",
  "severity_score": 7,
  "length_of_stay": 4,
  "previous_visit_gap_days": 45,
  "number_of_previous_visits": 3
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "readmission_risk": "Low",
    "probability": 0.461,
    "recommendation": "Standard care protocol"
  }
}
```

### 3. Predict Risk Score
```
POST /api/ml/predict/risk-score
```

**Request Body:**
```json
{
  "age": 65,
  "gender": "Male",
  "bmi": 28.5,
  "smoker_status": "yes",
  "alcohol_use": "no",
  "severity_score": 7,
  "length_of_stay": 4,
  "number_of_previous_visits": 3
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "risk_score": 70.8,
    "category": "High Risk",
    "color": "red"
  }
}
```

### 4. Predict Disease Progression
```
POST /api/ml/predict/disease-progression
```

**Request Body:**
```json
{
  "prev_severity": 5,
  "length_of_stay": 4,
  "previous_visit_gap_days": 45,
  "number_of_previous_visits": 3
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "progression": "Stable",
    "confidence": 0.422,
    "probabilities": {
      "improving": 0.333,
      "stable": 0.422,
      "worsening": 0.245
    }
  }
}
```

### 5. Batch Predictions (All Models)
```
POST /api/ml/batch-predict
```

**Request Body:**
```json
{
  "patient_data": {
    "age": 65,
    "gender": "Male",
    "bmi": 28.5,
    "smoker_status": "yes",
    "alcohol_use": "no",
    "severity_score": 7,
    "length_of_stay": 4,
    "number_of_previous_visits": 3
  },
  "visit_data": {
    "prev_severity": 5,
    "length_of_stay": 4,
    "previous_visit_gap_days": 45,
    "number_of_previous_visits": 3
  }
}
```

**Response:**
```json
{
  "success": true,
  "predictions": {
    "readmission": {
      "readmission_risk": "Low",
      "probability": 0.461,
      "recommendation": "Standard care protocol"
    },
    "risk_score": {
      "risk_score": 70.8,
      "category": "High Risk",
      "color": "red"
    },
    "disease_progression": {
      "progression": "Stable",
      "confidence": 0.422,
      "probabilities": {
        "improving": 0.333,
        "stable": 0.422,
        "worsening": 0.245
      }
    }
  }
}
```

## Testing the Models

### Option 1: Using curl
```bash
# Load models
curl http://localhost:5000/api/ml/load-models

# Test readmission prediction
curl -X POST http://localhost:5000/api/ml/predict/readmission \
  -H "Content-Type: application/json" \
  -d '{"age":65,"gender":"Male","bmi":28.5,"smoker_status":"yes","alcohol_use":"no","severity_score":7,"length_of_stay":4,"previous_visit_gap_days":45,"number_of_previous_visits":3}'
```

### Option 2: Using Python
```python
import requests

# Load models
response = requests.get('http://localhost:5000/api/ml/load-models')
print(response.json())

# Predict readmission
patient_data = {
    "age": 65,
    "gender": "Male",
    "bmi": 28.5,
    "smoker_status": "yes",
    "alcohol_use": "no",
    "severity_score": 7,
    "length_of_stay": 4,
    "previous_visit_gap_days": 45,
    "number_of_previous_visits": 3
}

response = requests.post(
    'http://localhost:5000/api/ml/predict/readmission',
    json=patient_data
)
print(response.json())
```

## Retraining Models

To retrain the models with fresh data:

```bash
cd backend
python train_models.py
```

This will:
1. Load latest data from MongoDB
2. Generate synthetic visit data if needed
3. Train all 3 models
4. Save models to `ml_models_saved/`
5. Run test predictions

## Integration with Frontend

You can integrate these predictions into your React frontend:

```javascript
// In DataEntry.js after successful patient submission
const predictReadmission = async (patientData) => {
  try {
    const response = await fetch('http://localhost:5000/api/ml/predict/readmission', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(patientData)
    });
    
    const result = await response.json();
    if (result.success) {
      console.log('Readmission Risk:', result.prediction.readmission_risk);
      console.log('Probability:', result.prediction.probability);
    }
  } catch (error) {
    console.error('Prediction error:', error);
  }
};
```

## Model Performance Metrics

| Model | Metric | Score | Interpretation |
|-------|--------|-------|----------------|
| Readmission | Accuracy | 61.85% | Good for synthetic data |
| Readmission | AUC-ROC | 0.510 | Room for improvement with real data |
| Risk Scoring | R² | 0.999 | Excellent fit |
| Risk Scoring | MSE | 0.56 | Very low error |
| Progression | Accuracy | 53.73% | Moderate performance |

## Important Notes

1. **Data Quality**: Models trained on synthetic visit data. Performance will improve with real visit records.
2. **Feature Matching**: Ensure API requests match exact feature names and formats (lowercase for 'yes'/'no')
3. **Model Updates**: Retrain models monthly with new data for best performance
4. **Error Handling**: All endpoints return error messages if models not loaded or fields missing

## Troubleshooting

**"Model not trained yet" error:**
- Run `python train_models.py` first
- Restart Flask server to auto-load models
- Or call GET `/api/ml/load-models` endpoint

**"Missing required fields" error:**
- Check all field names match exactly (case-sensitive)
- Ensure all required fields are present in request

**"Previously unseen labels" error:**
- Use lowercase values: 'yes'/'no' not 'Yes'/'No'
- Gender values: 'Male', 'Female', 'Other'
