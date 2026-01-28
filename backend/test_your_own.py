"""
Interactive ML Model Testing
Modify the patient data below and run this script to get predictions!
"""

import requests
import json

# 🎯 MODIFY THIS DATA TO TEST DIFFERENT PREDICTIONS
# Change the values below to see how predictions change!

# Test Case 1: Young healthy patient
young_patient = {
    "age": 25,
    "gender": "Female",
    "bmi": 22.0,
    "smoker_status": "no",
    "alcohol_use": "no",
    "severity_score": 2,
    "length_of_stay": 1,
    "previous_visit_gap_days": 180,
    "number_of_previous_visits": 0
}

# Test Case 2: Elderly high-risk patient
elderly_patient = {
    "age": 78,
    "gender": "Male",
    "bmi": 32.5,
    "smoker_status": "yes",
    "alcohol_use": "yes",
    "severity_score": 9,
    "length_of_stay": 10,
    "previous_visit_gap_days": 15,
    "number_of_previous_visits": 8
}

# Test Case 3: Middle-aged moderate risk
middle_aged_patient = {
    "age": 50,
    "gender": "Female",
    "bmi": 27.0,
    "smoker_status": "no",
    "alcohol_use": "yes",
    "severity_score": 5,
    "length_of_stay": 3,
    "previous_visit_gap_days": 90,
    "number_of_previous_visits": 2
}

# 📝 CHOOSE WHICH PATIENT TO TEST (change the variable name below)
# Options: young_patient, elderly_patient, middle_aged_patient
TEST_PATIENT = elderly_patient  # ← Change this to test different patients!

# ==============================================================
# TEST FUNCTIONS (You can modify these too!)
# ==============================================================

BASE_URL = 'http://localhost:5000'

def print_header(title):
    print("\n" + "="*60)
    print(f"   {title}")
    print("="*60)

def test_readmission(patient_data):
    print_header("🔮 30-DAY READMISSION PREDICTION")
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/ml/predict/readmission',
            json=patient_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                pred = result['prediction']
                print(f"\n   📊 Risk Level: {pred['readmission_risk']}")
                print(f"   📈 Probability: {pred['probability']:.1%}")
                print(f"   💡 Recommendation: {pred['recommendation']}")
            else:
                print(f"   ❌ Error: {result.get('message')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server!")
        print("   💡 Make sure backend is running: python app.py")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_risk_score(patient_data):
    print_header("🎯 HEALTH RISK SCORE (0-100)")
    
    # Remove fields not needed for risk score
    risk_data = {k: v for k, v in patient_data.items() 
                 if k != 'previous_visit_gap_days'}
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/ml/predict/risk-score',
            json=risk_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                pred = result['prediction']
                score = pred['risk_score']
                category = pred['category']
                color = pred['color']
                
                # Visual bar
                bar_length = int(score)
                bar = "█" * (bar_length // 2)
                
                print(f"\n   📊 Risk Score: {score:.1f}/100")
                print(f"   {bar}")
                print(f"   📌 Category: {category}")
                print(f"   🎨 Alert Level: {color}")
            else:
                print(f"   ❌ Error: {result.get('message')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server!")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_progression(patient_data):
    print_header("📈 DISEASE PROGRESSION FORECAST")
    
    # Prepare visit data for progression
    visit_data = {
        "prev_severity": patient_data.get('severity_score', 5) - 1,
        "length_of_stay": patient_data.get('length_of_stay', 3),
        "previous_visit_gap_days": patient_data.get('previous_visit_gap_days', 60),
        "number_of_previous_visits": patient_data.get('number_of_previous_visits', 1)
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/ml/predict/disease-progression',
            json=visit_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                pred = result['prediction']
                print(f"\n   📊 Trend: {pred['progression']}")
                print(f"   📈 Confidence: {pred['confidence']:.1%}")
                print(f"\n   📉 Detailed Probabilities:")
                for key, val in pred['probabilities'].items():
                    bar = "█" * int(val * 30)
                    print(f"      {key.capitalize():12} {val:5.1%} {bar}")
            else:
                print(f"   ❌ Error: {result.get('message')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server!")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# ==============================================================
# MAIN PROGRAM
# ==============================================================

if __name__ == "__main__":
    print("\n" + "🏥" * 30)
    print("   HEALTHCARE ML MODEL TESTING - YOUR OWN DATA")
    print("🏥" * 30)
    
    # Show patient info
    print("\n📋 PATIENT INFORMATION:")
    print("-" * 60)
    for key, value in TEST_PATIENT.items():
        print(f"   {key:28} : {value}")
    print("-" * 60)
    
    # Run all predictions
    test_readmission(TEST_PATIENT)
    test_risk_score(TEST_PATIENT)
    test_progression(TEST_PATIENT)
    
    # Summary
    print("\n" + "="*60)
    print("   ✅ TESTING COMPLETE!")
    print("="*60)
    print("\n💡 HOW TO TEST MORE:")
    print("   1. Edit the patient data at the top of this file")
    print("   2. Change TEST_PATIENT variable to different test cases")
    print("   3. Run again: python test_your_own.py")
    print("\n📝 FIELD REFERENCE:")
    print("   age: 0-120")
    print("   gender: Male, Female, Other")
    print("   bmi: 15.0-50.0 (normal: 18.5-24.9)")
    print("   smoker_status: yes, no")
    print("   alcohol_use: yes, no")
    print("   severity_score: 1-10 (1=mild, 10=critical)")
    print("   length_of_stay: 1-30 (days)")
    print("   previous_visit_gap_days: 0-365")
    print("   number_of_previous_visits: 0-20")
    print()
