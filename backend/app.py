from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from datetime import datetime
import boto3
from werkzeug.utils import secure_filename
import json
from dotenv import load_dotenv
from ml_models import HealthcareMLModels

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'healthcare_analytics')

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', 'sravani-healthcare-data')
AWS_REGION = os.getenv('AWS_REGION', 'eu-north-1')

# In-memory storage (for testing without MongoDB)
in_memory_db = {
    'patients': [],
    'visits': [],
    'prescriptions': [],
    'uploads': []
}

# Initialize MongoDB client
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    mongo_client.server_info()  # Force connection check
    db = mongo_client[MONGO_DB]
    analytics_collection = db['analytics']
    print(f"✅ Connected to MongoDB: {MONGO_DB}")
except Exception as e:
    print(f"⚠️  MongoDB not available, using in-memory storage")
    db = None

# Initialize AWS S3 client
try:
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        print(f"✅ Connected to AWS S3: {AWS_BUCKET_NAME}")
    else:
        s3_client = None
        print("⚠️  AWS credentials not configured")
except Exception as e:
    print(f"❌ AWS S3 connection failed: {e}")
    s3_client = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'mongodb': 'connected' if db is not None else 'disconnected',
        's3': 'connected' if s3_client is not None else 'disconnected'
    }), 200

# File Upload Endpoint
@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400

        file = request.files['file']
        file_type = request.form.get('type', 'unknown')

        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{file_type}_{timestamp}_{filename}"
            
            # Save file locally
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            # Upload to S3 if configured
            if s3_client:
                try:
                    s3_key = f"raw/{file_type}/{unique_filename}"
                    s3_client.upload_file(filepath, AWS_BUCKET_NAME, s3_key)
                    print(f"✅ File uploaded to S3: {s3_key}")
                except Exception as e:
                    print(f"⚠️  S3 upload failed: {e}")

            # Store metadata in MongoDB
            if db is not None:
                try:
                    db.uploads.insert_one({
                        'filename': unique_filename,
                        'original_filename': file.filename,
                        'type': file_type,
                        'upload_date': datetime.now(),
                        'size': os.path.getsize(filepath),
                        's3_uploaded': s3_client is not None
                    })
                except Exception as e:
                    print(f"⚠️  MongoDB insert failed: {e}")

            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'filename': unique_filename
            }), 200

        return jsonify({'success': False, 'message': 'Invalid file type'}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Patient Endpoints
@app.route('/api/patient', methods=['POST'])
def create_patient():
    try:
        data = request.json
        
        # ✅ VALIDATION - Job #2: Validate required fields
        required_fields = ['patient_id', 'age', 'gender', 'location']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False, 
                    'message': f'Missing required field: {field}'
                }), 400
        
        # ✅ VALIDATION - Check data types
        try:
            age = int(data['age'])
            if age < 0 or age > 150:
                return jsonify({
                    'success': False, 
                    'message': 'Age must be between 0 and 150'
                }), 400
        except ValueError:
            return jsonify({
                'success': False, 
                'message': 'Age must be a number'
            }), 400
        
        data['created_at'] = datetime.now().isoformat()
        data['updated_at'] = datetime.now().isoformat()

        # ✅ STORAGE - Job #3: Store data safely
        if db is not None:
            try:
                result = db.patients.insert_one(data.copy())
                print(f"✅ Patient stored in MongoDB: {data['patient_id']}")
                return jsonify({
                    'success': True,
                    'message': 'Patient created successfully',
                    'patient_id': str(result.inserted_id)
                }), 201
            except Exception as e:
                print(f"MongoDB error: {e}")
                # Fallback to in-memory storage
                data['_id'] = len(in_memory_db['patients']) + 1
                in_memory_db['patients'].append(data)
                print(f"✅ Patient stored in memory: {data['patient_id']}")
                return jsonify({
                    'success': True,
                    'message': 'Patient created successfully (in-memory)',
                    'patient_id': str(data['_id'])
                }), 201
        else:
            # Use in-memory storage
            data['_id'] = len(in_memory_db['patients']) + 1
            in_memory_db['patients'].append(data)
            print(f"✅ Patient stored in memory: {data['patient_id']}")
            return jsonify({
                'success': True,
                'message': 'Patient created successfully',
                'patient_id': str(data['_id'])
            }), 201

    except Exception as e:
        print(f"❌ Error creating patient: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        if db is not None:
            try:
                patients = list(db.patients.find({}, {'_id': 0}).limit(100))
                return jsonify({
                    'success': True,
                    'count': len(patients),
                    'patients': patients
                }), 200
            except:
                # Fallback to in-memory
                return jsonify({
                    'success': True,
                    'count': len(in_memory_db['patients']),
                    'patients': in_memory_db['patients']
                }), 200
        else:
            return jsonify({
                'success': True,
                'count': len(in_memory_db['patients']),
                'patients': in_memory_db['patients']
            }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Visit Endpoints
@app.route('/api/visit', methods=['POST'])
def create_visit():
    try:
        data = request.json
        
        # ✅ VALIDATION - Required fields
        required_fields = ['visit_id', 'patient_id', 'visit_date', 'diagnosis_code']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False, 
                    'message': f'Missing required field: {field}'
                }), 400
        
        data['created_at'] = datetime.now().isoformat()
        data['updated_at'] = datetime.now().isoformat()

        # ✅ STORAGE - Store visit data
        if db is not None:
            try:
                result = db.visits.insert_one(data.copy())
                print(f"✅ Visit stored in MongoDB: {data['visit_id']}")
                return jsonify({
                    'success': True,
                    'message': 'Visit created successfully',
                    'visit_id': str(result.inserted_id)
                }), 201
            except Exception as e:
                print(f"MongoDB error: {e}")
                data['_id'] = len(in_memory_db['visits']) + 1
                in_memory_db['visits'].append(data)
                print(f"✅ Visit stored in memory: {data['visit_id']}")
                return jsonify({
                    'success': True,
                    'message': 'Visit created successfully (in-memory)',
                    'visit_id': str(data['_id'])
                }), 201
        else:
            data['_id'] = len(in_memory_db['visits']) + 1
            in_memory_db['visits'].append(data)
            print(f"✅ Visit stored in memory: {data['visit_id']}")
            return jsonify({
                'success': True,
                'message': 'Visit created successfully',
                'visit_id': str(data['_id'])
            }), 201

    except Exception as e:
        print(f"Error creating visit: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/visits', methods=['GET'])
def get_visits():
    try:
        if db is not None:
            try:
                visits = list(db.visits.find({}, {'_id': 0}).limit(100))
                return jsonify({
                    'success': True,
                    'count': len(visits),
                    'visits': visits
                }), 200
            except:
                return jsonify({
                    'success': True,
                    'count': len(in_memory_db['visits']),
                    'visits': in_memory_db['visits']
                }), 200
        else:
            return jsonify({
                'success': True,
                'count': len(in_memory_db['visits']),
                'visits': in_memory_db['visits']
            }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Prescription Endpoints
@app.route('/api/prescription', methods=['POST'])
def create_prescription():
    try:
        data = request.json
        data['created_at'] = datetime.now().isoformat()
        data['updated_at'] = datetime.now().isoformat()

        if db is not None:
            try:
                result = db.prescriptions.insert_one(data.copy())
                return jsonify({
                    'success': True,
                    'message': 'Prescription created successfully',
                    'prescription_id': str(result.inserted_id)
                }), 201
            except Exception as e:
                print(f"MongoDB error: {e}")
                data['_id'] = len(in_memory_db['prescriptions']) + 1
                in_memory_db['prescriptions'].append(data)
                return jsonify({
                    'success': True,
                    'message': 'Prescription created successfully (in-memory)',
                    'prescription_id': str(data['_id'])
                }), 201
        else:
            data['_id'] = len(in_memory_db['prescriptions']) + 1
            in_memory_db['prescriptions'].append(data)
            return jsonify({
                'success': True,
                'message': 'Prescription created successfully',
                'prescription_id': str(data['_id'])
            }), 201

    except Exception as e:
        print(f"Error creating prescription: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    try:
        if db is not None:
            try:
                prescriptions = list(db.prescriptions.find({}, {'_id': 0}).limit(100))
                return jsonify({
                    'success': True,
                    'count': len(prescriptions),
                    'prescriptions': prescriptions
                }), 200
            except:
                return jsonify({
                    'success': True,
                    'count': len(in_memory_db['prescriptions']),
                    'prescriptions': in_memory_db['prescriptions']
                }), 200
        else:
            return jsonify({
                'success': True,
                'count': len(in_memory_db['prescriptions']),
                'prescriptions': in_memory_db['prescriptions']
            }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Dashboard Endpoint
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        if db is not None:
            try:
                # Get real counts from MongoDB
                patients_count = db.patients.count_documents({})
                visits_count = db.visits.count_documents({})
                prescriptions_count = db.prescriptions.count_documents({})
                
                # Calculate age distribution from real data
                age_pipeline = [
                    {
                        '$addFields': {
                            'ageGroup': {
                                '$switch': {
                                    'branches': [
                                        {'case': {'$lte': [{'$toInt': '$age'}, 18]}, 'then': '0-18'},
                                        {'case': {'$lte': [{'$toInt': '$age'}, 35]}, 'then': '19-35'},
                                        {'case': {'$lte': [{'$toInt': '$age'}, 50]}, 'then': '36-50'},
                                        {'case': {'$lte': [{'$toInt': '$age'}, 65]}, 'then': '51-65'},
                                    ],
                                    'default': '65+'
                                }
                            }
                        }
                    },
                    {'$group': {'_id': '$ageGroup', 'count': {'$sum': 1}}},
                    {'$project': {'ageGroup': '$_id', 'count': 1, '_id': 0}}
                ]
                
                age_dist = list(db.patients.aggregate(age_pipeline)) if patients_count > 0 else []
                
                # Calculate gender distribution from real data
                gender_pipeline = [
                    {'$group': {'_id': '$gender', 'value': {'$sum': 1}}},
                    {'$project': {'gender': '$_id', 'value': 1, '_id': 0}}
                ]
                
                gender_dist = list(db.patients.aggregate(gender_pipeline)) if patients_count > 0 else []
                
                # Calculate disease distribution from visits
                disease_pipeline = [
                    {'$group': {'_id': '$diagnosis_description', 'count': {'$sum': 1}}},
                    {'$sort': {'count': -1}},
                    {'$limit': 5},
                    {'$project': {'disease': '$_id', 'count': 1, '_id': 0}}
                ]
                
                disease_dist = list(db.visits.aggregate(disease_pipeline)) if visits_count > 0 else []
                
                # Calculate visit trends by month
                visit_trends_pipeline = [
                    {
                        '$addFields': {
                            'month': {
                                '$dateToString': {
                                    'format': '%b',
                                    'date': {'$toDate': '$visit_date'}
                                }
                            }
                        }
                    },
                    {'$group': {'_id': '$month', 'visits': {'$sum': 1}}},
                    {'$project': {'month': '$_id', 'visits': 1, '_id': 0}}
                ]
                
                visit_trends = list(db.visits.aggregate(visit_trends_pipeline)) if visits_count > 0 else []
                
                # Build dashboard data with real values or defaults
                dashboard_data = {
                    'summary': {
                        'totalPatients': patients_count,
                        'totalVisits': visits_count,
                        'totalPrescriptions': prescriptions_count,
                        'activeCases': max(1, int(visits_count * 0.3))
                    },
                    'ageDistribution': age_dist if age_dist else [
                        {'ageGroup': '0-18', 'count': 0},
                        {'ageGroup': '19-35', 'count': 0},
                        {'ageGroup': '36-50', 'count': 0},
                        {'ageGroup': '51-65', 'count': 0},
                        {'ageGroup': '65+', 'count': 0}
                    ],
                    'visitTrends': visit_trends if visit_trends else [
                        {'month': 'Jan', 'visits': 0}
                    ],
                    'diseaseDistribution': disease_dist if disease_dist else [
                        {'disease': 'No data', 'count': 0}
                    ],
                    'genderDistribution': gender_dist if gender_dist else [
                        {'gender': 'Male', 'value': 0},
                        {'gender': 'Female', 'value': 0}
                    ]
                }
                
                print(f"📊 Dashboard: {patients_count} patients, {visits_count} visits, {prescriptions_count} prescriptions")
                
                return jsonify({
                    'success': True,
                    'data': dashboard_data
                }), 200
            except Exception as e:
                print(f"MongoDB dashboard error: {e}")
                # Fallback to sample data
                pass
        
        # Use sample data for in-memory or MongoDB error
        dashboard_data = {
            'summary': {
                'totalPatients': len(in_memory_db['patients']),
                'totalVisits': len(in_memory_db['visits']),
                'totalPrescriptions': len(in_memory_db['prescriptions']),
                'activeCases': max(1, int(len(in_memory_db['visits']) * 0.3))
            },
            'ageDistribution': [
                {'ageGroup': '0-18', 'count': 45},
                {'ageGroup': '19-35', 'count': 120},
                {'ageGroup': '36-50', 'count': 180},
                {'ageGroup': '51-65', 'count': 150},
                {'ageGroup': '65+', 'count': 80}
            ],
            'visitTrends': [
                {'month': 'Jan', 'visits': 120},
                {'month': 'Feb', 'visits': 135},
                {'month': 'Mar', 'visits': 148},
                {'month': 'Apr', 'visits': 142},
                {'month': 'May', 'visits': 156},
                {'month': 'Jun', 'visits': 165}
            ],
            'diseaseDistribution': [
                {'disease': 'Hypertension', 'count': 230},
                {'disease': 'Diabetes', 'count': 189},
                {'disease': 'Asthma', 'count': 145},
                {'disease': 'Arthritis', 'count': 112},
                {'disease': 'Heart Disease', 'count': 98}
            ],
            'genderDistribution': [
                {'gender': 'Male', 'value': 52},
                {'gender': 'Female', 'value': 45},
                {'gender': 'Other', 'value': 3}
            ]
        }
        
        return jsonify({
            'success': True,
            'data': dashboard_data
        }), 200

    except Exception as e:
        print(f"Dashboard error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# =========================================================================
# MACHINE LEARNING PREDICTION ENDPOINTS
# =========================================================================

# Initialize ML models (will load trained models)
ml_models = HealthcareMLModels()

@app.route('/api/ml/load-models', methods=['GET'])
def load_ml_models():
    """Load the latest trained ML models"""
    try:
        success = ml_models.load_models()
        if success:
            return jsonify({
                'success': True,
                'message': 'ML models loaded successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No trained models found. Run train_models.py first.'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading models: {str(e)}'
        }), 500

@app.route('/api/ml/predict/readmission', methods=['POST'])
def predict_readmission():
    """
    Predict 30-day readmission risk
    
    Required fields:
    - age, gender, bmi, smoker_status, alcohol_use
    - severity_score, length_of_stay, previous_visit_gap_days, number_of_previous_visits
    """
    try:
        patient_data = request.json
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'bmi', 'smoker_status', 'alcohol_use',
            'severity_score', 'length_of_stay', 'previous_visit_gap_days',
            'number_of_previous_visits'
        ]
        
        missing_fields = [f for f in required_fields if f not in patient_data]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Make prediction
        result = ml_models.predict_readmission(patient_data)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'message': result['error']
            }), 400
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/ml/predict/risk-score', methods=['POST'])
def predict_risk_score():
    """
    Predict overall health risk score (0-100)
    
    Required fields:
    - age, gender, bmi, smoker_status, alcohol_use
    - severity_score, length_of_stay, number_of_previous_visits
    """
    try:
        patient_data = request.json
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'bmi', 'smoker_status', 'alcohol_use',
            'severity_score', 'length_of_stay', 'number_of_previous_visits'
        ]
        
        missing_fields = [f for f in required_fields if f not in patient_data]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Make prediction
        result = ml_models.predict_risk_score(patient_data)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'message': result['error']
            }), 400
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/ml/predict/disease-progression', methods=['POST'])
def predict_disease_progression():
    """
    Predict disease progression trend (Improving/Stable/Worsening)
    
    Required fields:
    - prev_severity, blood_pressure, glucose_level, heart_rate
    - length_of_stay,length_of_stay, previous_visit_gap_days, number_of_previous_visits
    """
    try:
        visit_data = request.json
        
        # Validate required fields
        required_fields = [
            'prev_severity', 'length_of_stay', 'previous_visit_gap_days',
            'number_of_previous_visits'
        ]
        
        missing_fields = [f for f in required_fields if f not in visit_data]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Make prediction
        result = ml_models.predict_disease_progression(visit_data)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'message': result['error']
            }), 400
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/ml/batch-predict', methods=['POST'])
def batch_predict():
    """
    Make all three predictions for a patient in one request
    
    Required fields: Combination of all prediction endpoints
    """
    try:
        data = request.json
        patient_data = data.get('patient_data', {})
        visit_data = data.get('visit_data', {})
        
        # Merge data for readmission and risk score (they need patient + visit data)
        readmission_data = {**patient_data, **visit_data}
        risk_score_data = {**patient_data, **{k: v for k, v in visit_data.items() if k != 'prev_severity' and k != 'previous_visit_gap_days'}}
        
        results = {}
        
        # Try readmission prediction
        try:
            readmission = ml_models.predict_readmission(readmission_data)
            if 'error' not in readmission:
                results['readmission'] = readmission
            else:
                results['readmission'] = {'error': readmission['error']}
        except Exception as e:
            results['readmission'] = {'error': str(e)}
        
        # Try risk score prediction
        try:
            risk_score = ml_models.predict_risk_score(risk_score_data)
            if 'error' not in risk_score:
                results['risk_score'] = risk_score
            else:
                results['risk_score'] = {'error': risk_score['error']}
        except Exception as e:
            results['risk_score'] = {'error': str(e)}
        
        # Try disease progression prediction
        try:
            progression = ml_models.predict_disease_progression(visit_data)
            if 'error' not in progression:
                results['disease_progression'] = progression
            else:
                results['disease_progression'] = {'error': progression['error']}
        except Exception as e:
            results['disease_progression'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'readmission': results.get('readmission', {}),
            'risk_score': results.get('risk_score', {}),
            'disease_progression': results.get('disease_progression', {})
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/get-analytics', methods=['GET'])
def get_analytics():
    """
    Get analytics data calculated from PySpark processing
    """
    try:
        analytics_data = analytics_collection.find_one({}, {'_id': 0})
        
        if analytics_data:
            return jsonify({
                'success': True,
                'analytics': analytics_data
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No analytics data found. Run pyspark_processor.py first.'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Healthcare Analytics Backend Server...")
    print(f"📊 MongoDB: {'✅ Connected' if db is not None else '❌ Not connected'}")
    print(f"☁️  AWS S3: {'✅ Connected' if s3_client is not None else '❌ Not connected'}")
    print("🧠 ML Models: Attempting to load...")
    
    # Try to load ML models at startup
    try:
        if ml_models.load_models():
            print("🧠 ML Models: ✅ Loaded successfully")
        else:
            print("🧠 ML Models: ⚠️  Not found (run train_models.py to train)")
    except Exception as e:
        print(f"🧠 ML Models: ⚠️  {e}")
    
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=5000)
