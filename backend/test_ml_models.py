"""
Quick ML Model Testing Script
Run this after starting app.py to test all ML endpoints
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

print("="*60)
print("🧪 Testing ML Models")
print("="*60)

# Test 1: Load models
print("\n1️⃣ Testing model loading...")
try:
    response = requests.get(f'{BASE_URL}/api/ml/load-models')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("   Make sure backend server is running: python app.py")
    exit(1)

# Test 2: Readmission prediction
print("\n2️⃣ Testing readmission prediction...")
readmission_data = {
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

try:
    response = requests.post(
        f'{BASE_URL}/api/ml/predict/readmission',
        json=readmission_data
    )
    result = response.json()
    print(f"   Status: {response.status_code}")
    if result.get('success'):
        pred = result['prediction']
        print(f"   ✅ Readmission Risk: {pred['readmission_risk']}")
        print(f"   ✅ Probability: {pred['probability']:.1%}")
        print(f"   ✅ Recommendation: {pred['recommendation']}")
    else:
        print(f"   ❌ Error: {result.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Risk score prediction
print("\n3️⃣ Testing risk score prediction...")
risk_data = {
    "age": 65,
    "gender": "Male",
    "bmi": 28.5,
    "smoker_status": "yes",
    "alcohol_use": "no",
    "severity_score": 7,
    "length_of_stay": 4,
    "number_of_previous_visits": 3
}

try:
    response = requests.post(
        f'{BASE_URL}/api/ml/predict/risk-score',
        json=risk_data
    )
    result = response.json()
    print(f"   Status: {response.status_code}")
    if result.get('success'):
        pred = result['prediction']
        print(f"   ✅ Risk Score: {pred['risk_score']:.1f}/100")
        print(f"   ✅ Category: {pred['category']}")
        print(f"   ✅ Color: {pred['color']}")
    else:
        print(f"   ❌ Error: {result.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Disease progression prediction
print("\n4️⃣ Testing disease progression prediction...")
progression_data = {
    "prev_severity": 5,
    "length_of_stay": 4,
    "previous_visit_gap_days": 45,
    "number_of_previous_visits": 3
}

try:
    response = requests.post(
        f'{BASE_URL}/api/ml/predict/disease-progression',
        json=progression_data
    )
    result = response.json()
    print(f"   Status: {response.status_code}")
    if result.get('success'):
        pred = result['prediction']
        print(f"   ✅ Progression: {pred['progression']}")
        print(f"   ✅ Confidence: {pred['confidence']:.1%}")
        print(f"   ✅ Probabilities:")
        for key, val in pred['probabilities'].items():
            print(f"      - {key.capitalize()}: {val:.1%}")
    else:
        print(f"   ❌ Error: {result.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Batch prediction
print("\n5️⃣ Testing batch prediction (all models)...")
batch_data = {
    "patient_data": {
        "age": 72,
        "gender": "Female",
        "bmi": 31.2,
        "smoker_status": "yes",
        "alcohol_use": "yes",
        "severity_score": 8,
        "length_of_stay": 6,
        "previous_visit_gap_days": 30,
        "number_of_previous_visits": 5
    },
    "visit_data": {
        "prev_severity": 6,
        "length_of_stay": 6,
        "previous_visit_gap_days": 30,
        "number_of_previous_visits": 5
    }
}

try:
    response = requests.post(
        f'{BASE_URL}/api/ml/batch-predict',
        json=batch_data
    )
    result = response.json()
    print(f"   Status: {response.status_code}")
    if result.get('success'):
        print("   ✅ Batch Predictions:")
        
        if 'readmission' in result['predictions']:
            r = result['predictions']['readmission']
            print(f"      Readmission: {r.get('readmission_risk')} ({r.get('probability', 0):.1%})")
        
        if 'risk_score' in result['predictions']:
            r = result['predictions']['risk_score']
            print(f"      Risk Score: {r.get('risk_score', 0):.1f}/100 ({r.get('category')})")
        
        if 'disease_progression' in result['predictions']:
            r = result['predictions']['disease_progression']
            print(f"      Progression: {r.get('progression')} ({r.get('confidence', 0):.1%})")
    else:
        print(f"   ❌ Error: {result.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ ML Model Testing Complete!")
print("="*60)
print("\n💡 Tips:")
print("   - All models are working if you see ✅ symbols above")
print("   - Try different input values to see predictions change")
print("   - Check backend/ML_MODELS_README.md for full API docs")
