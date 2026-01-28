"""
Comprehensive System Test for Healthcare Analytics Platform
Tests: Backend, ML Models, S3, MongoDB, and all API endpoints
"""

import requests
import boto3
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import time

load_dotenv()

# Configuration
BASE_URL = "http://localhost:5000/api"
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.getenv('AWS_BUCKET_NAME', 'sravani-healthcare-data')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'healthcare_analytics')

print("="*70)
print("🧪 COMPREHENSIVE SYSTEM TEST")
print("="*70)

# Wait for server to be ready
print("\n⏳ Waiting for backend server...")
time.sleep(2)

# Test 1: Backend Server Health
print("\n📍 TEST 1: Backend Server Health")
try:
    response = requests.get(f"{BASE_URL}/patients", timeout=5)
    if response.status_code in [200, 404]:
        print("   ✅ Backend server is running")
    else:
        print(f"   ⚠️  Backend responded with status {response.status_code}")
except Exception as e:
    print(f"   ❌ Backend server not accessible: {e}")
    print("   ⚠️  Make sure backend is running: python app.py")

# Test 2: S3 Data Storage
print("\n📍 TEST 2: S3 Cleaned Data Files")
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    
    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET, Prefix='processed/cleaned/')
    files = response.get('Contents', [])
    
    if files:
        print(f"   ✅ Found {len(files)} cleaned CSV files in S3:")
        for obj in files:
            size_kb = obj['Size'] / 1024
            print(f"      - {obj['Key']} ({size_kb:.2f} KB)")
    else:
        print("   ❌ No cleaned files found in S3")
except Exception as e:
    print(f"   ❌ S3 error: {e}")

# Test 3: MongoDB Data
print("\n📍 TEST 3: MongoDB Collections")
try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    
    collections = {
        'patients_processed': db.patients_processed.count_documents({}),
        'visits_processed': db.visits_processed.count_documents({}),
        'prescriptions_processed': db.prescriptions_processed.count_documents({}),
        'analytics': db.analytics.count_documents({})
    }
    
    print("   ✅ MongoDB Collections:")
    for coll, count in collections.items():
        print(f"      - {coll}: {count} documents")
    
    client.close()
except Exception as e:
    print(f"   ❌ MongoDB error: {e}")

# Test 4: ML Model Loading
print("\n📍 TEST 4: ML Models Loading")
try:
    response = requests.get(f"{BASE_URL}/ml/load-models")
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Models loaded: {data.get('models_timestamp')}")
            models = data.get('models_loaded', [])
            for model in models:
                print(f"      - {model}")
        else:
            print(f"   ❌ Model loading failed: {data.get('error')}")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Readmission Prediction
print("\n📍 TEST 5: Readmission Prediction Endpoint")
try:
    test_data = {
        "age": 65,
        "gender": "Male",
        "bmi": 28.5,
        "smoker_status": "yes",
        "alcohol_use": "no",
        "severity_score": 7,
        "length_of_stay": 5,
        "previous_visit_gap_days": 45,
        "number_of_previous_visits": 3
    }
    
    response = requests.post(f"{BASE_URL}/ml/predict/readmission", json=test_data)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            pred = data['prediction']
            print(f"   ✅ Readmission Prediction:")
            print(f"      - Risk: {pred['readmission_risk']}")
            print(f"      - Probability: {pred['probability']:.1f}%")
            print(f"      - Recommendation: {pred['recommendation']}")
        else:
            print(f"   ❌ Prediction failed: {data.get('error')}")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Risk Score Prediction
print("\n📍 TEST 6: Risk Score Prediction Endpoint")
try:
    test_data = {
        "age": 72,
        "gender": "Female",
        "bmi": 32.0,
        "smoker_status": "yes",
        "alcohol_use": "yes",
        "severity_score": 9,
        "length_of_stay": 12,
        "number_of_previous_visits": 8
    }
    
    response = requests.post(f"{BASE_URL}/ml/predict/risk-score", json=test_data)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            pred = data['prediction']
            print(f"   ✅ Risk Score Prediction:")
            print(f"      - Score: {pred['risk_score']:.1f}/100")
            print(f"      - Category: {pred['category']}")
        else:
            print(f"   ❌ Prediction failed: {data.get('error')}")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 7: Disease Progression Prediction
print("\n📍 TEST 7: Disease Progression Prediction Endpoint")
try:
    test_data = {
        "prev_severity": 5,
        "length_of_stay": 7,
        "previous_visit_gap_days": 60,
        "number_of_previous_visits": 4
    }
    
    response = requests.post(f"{BASE_URL}/ml/predict/disease-progression", json=test_data)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            pred = data['prediction']
            print(f"   ✅ Disease Progression Prediction:")
            print(f"      - Progression: {pred['progression']}")
            print(f"      - Confidence: {pred['confidence']:.1f}%")
        else:
            print(f"   ❌ Prediction failed: {data.get('error')}")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 8: Batch Prediction
print("\n📍 TEST 8: Batch Prediction Endpoint")
try:
    test_data = {
        "patient_data": {
            "age": 55,
            "gender": "Male",
            "bmi": 27.0,
            "smoker_status": "no",
            "alcohol_use": "no"
        },
        "visit_data": {
            "severity_score": 5,
            "length_of_stay": 4,
            "previous_visit_gap_days": 90,
            "number_of_previous_visits": 2,
            "prev_severity": 4
        }
    }
    
    response = requests.post(f"{BASE_URL}/ml/batch-predict", json=test_data)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Batch Prediction:")
            print(f"      - Readmission: {data.get('readmission', {}).get('readmission_risk', 'N/A')}")
            print(f"      - Risk Score: {data.get('risk_score', {}).get('risk_score', 'N/A')}")
            print(f"      - Progression: {data.get('disease_progression', {}).get('progression', 'N/A')}")
        else:
            print(f"   ❌ Prediction failed: {data.get('message')}")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 9: Patients Endpoint
print("\n📍 TEST 9: Patients API Endpoint")
try:
    response = requests.get(f"{BASE_URL}/patients?limit=5")
    if response.status_code == 200:
        data = response.json()
        count = len(data.get('patients', []))
        print(f"   ✅ Retrieved {count} patients")
        if count > 0:
            sample = data['patients'][0]
            print(f"      Sample: {sample.get('patient_id')} - Age {sample.get('age')}, {sample.get('gender')}")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 10: Analytics Endpoint
print("\n📍 TEST 10: Analytics Endpoint")
try:
    response = requests.get(f"{BASE_URL}/get-analytics")
    if response.status_code == 200:
        data = response.json()
        analytics = data.get('analytics', {})
        print(f"   ✅ Analytics Retrieved:")
        
        age_groups = analytics.get('age_distribution', [])
        if age_groups:
            print(f"      - Age Groups: {len(age_groups)} groups")
        
        gender_dist = analytics.get('gender_distribution', [])
        if gender_dist:
            print(f"      - Gender Distribution: {len(gender_dist)} categories")
        
        diseases = analytics.get('disease_distribution', [])
        if diseases:
            print(f"      - Top Diseases: {len(diseases)} tracked")
            if diseases:
                print(f"         Top: {diseases[0].get('disease')} ({diseases[0].get('count')} cases)")
    else:
        print(f"   ❌ HTTP {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "="*70)
print("✅ TESTING COMPLETE!")
print("="*70)
print("\n📊 Components Tested:")
print("   1. Backend Server Health")
print("   2. S3 Data Storage (cleaned CSVs)")
print("   3. MongoDB Collections")
print("   4. ML Model Loading")
print("   5. Readmission Prediction")
print("   6. Risk Score Prediction")
print("   7. Disease Progression Prediction")
print("   8. Batch Prediction")
print("   9. Patients API")
print("   10. Analytics API")
print("\n💡 Review results above for any ❌ failures")
