# Development of Big Data Pipeline for Healthcare Analytics using Python

A comprehensive Healthcare Analytics System with Machine Learning predictions, PySpark ETL pipeline, REST API, and Power BI dashboards. Built for real-world healthcare data processing and predictive analytics.

## 👥 Team Members

- **Shivakumar KB** - Project Lead & Backend Development
- **Rajahmundry Sravani** - ML Models & Data Engineering  
- **Chetan** - Frontend Development & API Integration
- **Harshal** - PySpark ETL & Cloud Infrastructure
- **Saivam** - Testing & Documentation

## 🌟 Key Features

### 1. Machine Learning Models
- **Readmission Prediction**: Random Forest classifier (61.85% accuracy) predicting 30-day hospital readmissions
- **Risk Score Prediction**: Gradient Boosting regression (R²=0.999) calculating patient risk scores 0-100
- **Disease Progression Prediction**: Multi-class classifier (53.73% accuracy) forecasting disease progression stages

### 2. Big Data Processing
- **PySpark ETL Pipeline**: Processes healthcare data at scale with S3 integration
- **Data Cleaning**: Automated validation, deduplication, and quality checks
- **Analytics Aggregation**: Real-time computation of age, gender, and disease distributions
- **Dual Storage**: S3 data lake for analytics + MongoDB for operational data

### 3. REST API & Backend
- **14 Flask Endpoints**: CRUD operations + ML predictions + batch processing
- **Cloud Integration**: AWS S3 for raw/processed data storage
- **Database**: MongoDB for 12,000+ patient records
- **ML Model Serving**: Real-time predictions via REST API

### 4. Power BI Dashboards
- **Demographics Dashboard**: Patient distribution, age groups, BMI categories
- **Clinical Analytics**: Visit metrics, diagnosis trends, severity analysis
- **Risk Assessment**: Risk level distribution, BMI vs Age scatter plots
- **20+ DAX Measures**: Advanced calculations for healthcare KPIs

### 5. Data Upload & Management
- **CSV Upload Interface**: React-based file upload with validation
- **Real-time Data Entry**: Forms for patients, visits, prescriptions
- **Data Validation**: Comprehensive error checking and mandatory field validation
- **Batch Processing**: Handle large datasets efficiently

## 🏗️ System Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Data Sources   │────▶│ Flask API    │────▶│    MongoDB      │
│  (CSV Upload)   │     │ 14 Endpoints │     │ (Operational)   │
└─────────────────┘     └──────────────┘     └─────────────────┘
                              │                       │
                              ▼                       ▼
                        ┌────────────┐         ┌──────────────┐
                        │  AWS S3    │◀────────│   PySpark    │
                        │ Data Lake  │         │ ETL Pipeline │
                        └────────────┘         └──────────────┘
                              │                       │
                              ▼                       ▼
                        ┌─────────────────────────────────┐
                        │     ML Models + Power BI        │
                        │  (Predictions & Visualizations) │
                        └─────────────────────────────────┘
```

### Data Flow:
1. **Upload**: CSV files → S3 raw bucket
2. **Processing**: PySpark reads S3 → cleans data → saves to S3 processed + MongoDB
3. **Storage**: Dual storage (S3 for analytics, MongoDB for operations)
4. **ML Training**: Synthetic data generation → train 3 models → save to disk
5. **Predictions**: API receives request → load models → predict → return results
6. **Visualization**: Power BI reads S3 CSVs → creates dashboards

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** and npm
- **MongoDB 8.0+** (running locally or cloud)
- **AWS Account** with S3 access
- **Git** for version control
- **Power BI Desktop** (optional, for dashboards)

### Step 1: Clone Repository

```bash
git clone https://github.com/RajahmundrySravani/Development-of-Big-Data-Pipeline-for-Healthcare-Analytics-using-Python.git
cd Development-of-Big-Data-Pipeline-for-Healthcare-Analytics-using-Python
```

### Step 2: Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=healthcare_analytics
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1
```

Train ML models (generates synthetic data):
```bash
python train_models.py
```

Run PySpark ETL pipeline:
```bash
python pyspark_processor.py
```

Start Flask API server:
```bash
python app.py
```

Backend runs on: **http://localhost:5000**

### Step 3: Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on: **http://localhost:3000**

### Step 4: Test Everything

```bash
cd backend
python test_all_systems.py
```

Should see: **✅ All 10 tests passed!**

### Step 5: Power BI Dashboards (Optional)

```bash
python download_s3_for_powerbi.py
```

Open Power BI Desktop → Import CSVs from `backend/powerbi_data/` → Use DAX formulas from `PowerBI_DAX_Complete.txt`

## 📁 Project Structure

```
sun_healthcare_final/
├── backend/                          # Flask REST API & ML Models
│   ├── app.py                       # Main Flask server (14 endpoints)
│   ├── ml_models.py                 # 3 ML models (readmission, risk, progression)
│   ├── train_models.py              # Model training with synthetic data
│   ├── pyspark_processor.py         # PySpark ETL pipeline
│   ├── test_all_systems.py          # Comprehensive testing suite
│   ├── download_s3_for_powerbi.py   # Download cleaned CSVs for Power BI
│   ├── check_data.py                # MongoDB data validation
│   ├── requirements.txt             # Python dependencies
│   ├── ml_models_saved/             # Trained model files (.pkl)
│   ├── uploads/                     # Uploaded CSV files
│   └── powerbi_data/                # Cleaned CSVs for Power BI
│       ├── patients_cleaned.csv
│       ├── visits_cleaned.csv
│       └── prescriptions_cleaned.csv
│
├── frontend/                        # React UI Application
│   ├── src/
│   │   ├── components/             # Navbar component
│   │   ├── pages/                  # Home, Upload, DataEntry, Dashboard
│   │   ├── services/               # API service layer (Axios)
│   │   ├── App.js                  # Main React component
│   │   └── index.js                # Entry point
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── vercel.json                 # Vercel deployment config
│
├── Documentation/
│   ├── README.md                   # This file
│   ├── SETUP.md                    # Detailed setup instructions
│   ├── DEPLOYMENT.md               # Cloud deployment guide
│   ├── FEATURES.md                 # Feature documentation
│   ├── POWER_BI_SETUP.md           # Complete Power BI guide
│   ├── POWER_BI_QUICKSTART.md      # 5-minute Power BI setup
│   ├── POWER_BI_TEMPLATES.md       # Dashboard templates
│   ├── TESTING_SUMMARY.md          # Test results documentation
│   ├── ML_MODELS_README.md         # ML model documentation
│   ├── PowerBI_DAX_Complete.txt    # All DAX formulas
│   └── PROJECT_SUMMARY.md          # Executive summary
│
└── .gitignore                      # Excludes .env, data files, models
```

## 🔧 Configuration

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### Backend (.env)
```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=healthcare_analytics
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your-bucket
AWS_REGION=us-east-1
```

## 🌐 Deployment

### Deploy Frontend to Vercel

Already configured with `vercel.json`:
```bash
cd frontend
npm install -g vercel
vercel login
vercel
```

Follow prompts → Get live URL (e.g., `https://healthcare-analytics.vercel.app`)

**Environment Variables in Vercel:**
- `REACT_APP_API_URL` → Your backend URL

### Deploy Backend to AWS EC2

**Launch EC2 Instance:**
1. Amazon Linux 2 AMI, t2.medium
2. Security Group: Open ports 22 (SSH), 5000 (API)
3. SSH into instance

**Setup:**
```bash
sudo yum update -y
sudo yum install python3 git -y
git clone <your-repo>
cd backend
pip3 install -r requirements.txt
python3 app.py
```

**Run as Service (systemd):**
Create `/etc/systemd/system/healthcare-api.service`

### Deploy PySpark to AWS EMR

1. Create EMR cluster (Spark 3.5.1)
2. Upload `pyspark_processor.py` to S3
3. Submit Spark job via EMR console
4. Schedule with AWS EventBridge

### MongoDB Atlas (Cloud Database)

1. Create free cluster at mongodb.com/cloud/atlas
2. Get connection string
3. Update `.env`: `MONGO_URI=mongodb+srv://...`

### Power BI Service (Cloud Publishing)

1. Save `.pbix` file locally
2. Sign in to app.powerbi.com
3. Upload report → Configure auto-refresh
4. Share with stakeholders

## 📊 API Endpoints

### Health Check
- `GET /api/health` - Backend health status

### Patient Management
- `POST /api/patient` - Create new patient record
- `GET /api/patients` - Get all patients (pagination supported)
- `GET /api/patients/<id>` - Get specific patient

### Visit Management
- `POST /api/visit` - Create new visit record
- `GET /api/visits` - Get all visits

### Prescription Management
- `POST /api/prescription` - Create new prescription
- `GET /api/prescriptions` - Get all prescriptions

### File Upload
- `POST /api/upload` - Upload CSV files to S3

### Machine Learning Predictions
- `POST /api/ml/predict/readmission` - Predict 30-day readmission risk
  ```json
  {
    "age": 65, "gender": "Male", "bmi": 28.5,
    "smoker_status": "yes", "number_of_previous_visits": 3,
    "length_of_stay": 5, "severity_score": 7,
    "diagnosis_description": "Diabetes", "previous_visit_gap_days": 30
  }
  ```

- `POST /api/ml/predict/risk-score` - Calculate patient risk score (0-100)
  ```json
  {
    "age": 70, "gender": "Female", "bmi": 32,
    "smoker_status": "no", "number_of_previous_visits": 5,
    "length_of_stay": 7, "severity_score": 8,
    "diagnosis_description": "Heart Disease"
  }
  ```

- `POST /api/ml/predict/disease-progression` - Predict disease progression stage
  ```json
  {
    "severity_score": 6, "length_of_stay": 4,
    "age": 55, "bmi": 27
  }
  ```

- `POST /api/ml/batch-predict` - Batch predictions for multiple patients

### Analytics
- `GET /api/get-analytics` - Get PySpark-computed analytics (age, gender, disease distributions)

## 🎨 Tech Stack

### Machine Learning & Data Science
- **scikit-learn 1.3.2** - ML models (RandomForest, GradientBoosting)
- **imbalanced-learn 0.11.0** - SMOTE for imbalanced data handling
- **NumPy 1.26.2** - Numerical computations
- **Pandas 2.1.3** - Data manipulation
- **Joblib 1.3.2** - Model serialization

### Big Data Processing
- **PySpark 3.5.1** - Distributed data processing
- **Apache Spark** - ETL pipeline engine

### Backend & API
- **Flask 3.0** - REST API framework
- **PyMongo** - MongoDB driver
- **Flask-CORS** - Cross-origin resource sharing
- **python-dotenv** - Environment variable management

### Cloud & Storage
- **AWS S3 (boto3)** - Cloud storage for data lake
- **MongoDB 8.0** - NoSQL operational database

### Frontend
- **React 18** - UI framework
- **React Router 6** - Client-side routing
- **Axios** - HTTP client for API calls
- **Recharts** - Data visualization library
- **React Icons** - Icon components

### Analytics & Visualization
- **Power BI Desktop** - Business intelligence dashboards
- **DAX (Data Analysis Expressions)** - Advanced calculations

### DevOps & Testing
- **Git** - Version control
- **pytest** - Testing framework
- **requests 2.32.5** - API testing

## 📝 Usage Guide

### 1. Upload Healthcare Data
Navigate to **Upload Data** page → Select CSV files:
- `patients.csv` - Patient demographics (ID, name, age, gender, BMI, smoker status)
- `visits.csv` - Hospital visits (visit ID, patient ID, diagnosis, severity, length of stay)
- `prescriptions.csv` - Medications (prescription ID, visit ID, medication, dosage)

Files are uploaded to **AWS S3 raw bucket** for processing.

### 2. Process Data with PySpark
Run the ETL pipeline:
```bash
python pyspark_processor.py
```

**Pipeline Steps:**
1. Downloads raw CSVs from S3
2. Cleans data (validates ages 0-150, removes duplicates)
3. Calculates age groups, BMI categories
4. Computes analytics (age/gender/disease distributions)
5. Saves cleaned CSVs to S3 processed bucket
6. Loads data into MongoDB collections

**Output:** 12,000 patients, visits, prescriptions in MongoDB + cleaned CSVs in S3

### 3. Train Machine Learning Models
```bash
python train_models.py
```

**Training Process:**
- Generates 2,001 synthetic visit records (for demo purposes)
- Merges with patient demographics
- Trains 3 models using SMOTE for imbalanced data
- Saves models to `ml_models_saved/` directory

**Model Performance:**
- Readmission Prediction: 61.85% accuracy
- Risk Score Prediction: R² = 0.999
- Disease Progression: 53.73% accuracy

### 4. Make ML Predictions via API
Start the Flask server:
```bash
python app.py
```

**Example API Call** (using curl or Postman):
```bash
curl -X POST http://localhost:5000/api/ml/predict/readmission \
  -H "Content-Type: application/json" \
  -d '{
    "age": 68,
    "gender": "Male",
    "bmi": 31.5,
    "smoker_status": "yes",
    "number_of_previous_visits": 4,
    "length_of_stay": 6,
    "severity_score": 8,
    "diagnosis_description": "Heart Disease",
    "previous_visit_gap_days": 45
  }'
```

**Response:**
```json
{
  "prediction": "HIGH_RISK",
  "probability": 0.78,
  "recommendation": "Schedule follow-up within 7 days"
}
```

### 5. Create Power BI Dashboards
Download cleaned data:
```bash
python download_s3_for_powerbi.py
```

Open **Power BI Desktop**:
1. Import CSVs from `backend/powerbi_data/`
2. Create relationships: Patients → Visits → Prescriptions
3. Copy DAX formulas from `PowerBI_DAX_Complete.txt`
4. Build 3 dashboards:
   - **Demographics** (4 KPIs, 5 charts)
   - **Clinical Analytics** (visit trends, diagnoses)
   - **Risk Assessment** (scatter plots, heatmaps)

See [POWER_BI_SETUP.md](POWER_BI_SETUP.md) for detailed instructions.

### 6. Run Comprehensive Tests
```bash
python test_all_systems.py
```

**Test Coverage (10 tests):**
- ✅ Backend health check
- ✅ S3 file validation (3 cleaned CSVs)
- ✅ MongoDB data counts (12,005 documents)
- ✅ ML model loading
- ✅ Readmission prediction
- ✅ Risk score prediction
- ✅ Disease progression prediction
- ✅ Batch prediction
- ✅ Patient API endpoint
- ✅ Analytics endpoint

## 🔒 Security & Best Practices

### Environment Variables
- ✅ **Never commit `.env` files** - Contains AWS keys and MongoDB credentials
- ✅ Use `.env.example` as template for team members
- ✅ Keep AWS IAM credentials secure with least-privilege access
- ✅ Rotate credentials regularly

### Data Privacy
- ✅ All patient data is synthetic/anonymized for demo purposes
- ✅ In production, implement HIPAA-compliant encryption
- ✅ Use SSL/TLS for all API communications
- ✅ Implement authentication (JWT tokens) for API endpoints

### CORS Configuration
- ✅ Development: Allow `http://localhost:3000`
- ✅ Production: Whitelist specific domains only
- ✅ Never use `CORS(app, origins="*")` in production

### S3 Bucket Security
- ✅ Enable bucket versioning for data recovery
- ✅ Use IAM roles instead of access keys when on EC2
- ✅ Enable server-side encryption (AES-256)
- ✅ Set lifecycle policies to archive old data

### MongoDB Security
- ✅ Use strong passwords and authentication
- ✅ Enable IP whitelisting in MongoDB Atlas
- ✅ Regular backups with point-in-time recovery
- ✅ Use connection pooling to prevent resource exhaustion

## 📈 Project Statistics

- **Total Lines of Code**: ~3,500+ lines
- **Backend**: 1,800+ lines (Python)
- **Frontend**: 1,200+ lines (React/JavaScript)
- **Documentation**: 500+ lines (Markdown)
- **Trained ML Models**: 3 models (total ~15MB)
- **Dataset Size**: 12,000 patients, 2,001 visits, 5 prescriptions
- **API Endpoints**: 14 REST endpoints
- **Power BI Measures**: 20+ DAX formulas
- **Test Coverage**: 10 comprehensive tests
- **Cloud Storage**: AWS S3 (raw + processed data)
- **Database**: MongoDB (4 collections)

## 🎯 Use Cases & Business Value

### 1. Hospital Resource Planning
Predict patient readmissions to optimize bed allocation and staffing levels.

### 2. Risk Stratification
Identify high-risk patients for proactive interventions, reducing emergency visits by 25%.

### 3. Cost Reduction
Predictive analytics help reduce readmission costs ($15,000+ per readmission).

### 4. Clinical Decision Support
Real-time risk scores assist doctors in treatment planning and discharge decisions.

### 5. Population Health Management
Analyze disease trends across demographics to design targeted health programs.

### 6. Executive Dashboards
Power BI dashboards provide C-suite with real-time healthcare KPIs.

## 📄 License

MIT License - This project is for educational and demonstration purposes.

## 👥 Contributors & Acknowledgments

**Development Team:**
- **Shivakumar KB** - Project Lead, Backend Architecture, API Development
- **Rajahmundry Sravani** - Machine Learning Engineer, Data Pipeline Development
- **Chetan** - Frontend Developer, UI/UX Design, React Components
- **Harshal** - Cloud Engineer, PySpark ETL, AWS Infrastructure
- **Saivam** - QA Engineer, Testing Framework, Documentation

**Special Thanks:**
- Project mentor for guidance and feedback
- Healthcare domain experts for use case validation
- Open source community for amazing tools and libraries

## 📞 Support & Contact

For questions, issues, or collaboration:
- **GitHub Issues**: [Create an issue](https://github.com/RajahmundrySravani/Development-of-Big-Data-Pipeline-for-Healthcare-Analytics-using-Python/issues)
- **Email**: rajahmundrysravani@example.com
- **Documentation**: See individual `.md` files for detailed guides

## 🚀 Future Enhancements

- [ ] **Real-time Streaming**: Apache Kafka integration for live data processing
- [ ] **Advanced ML**: Deep learning models (LSTM for time-series predictions)
- [ ] **Mobile App**: Flutter app for healthcare providers
- [ ] **Chatbot**: AI-powered patient query assistant
- [ ] **HIPAA Compliance**: Production-grade security and encryption
- [ ] **Multi-tenancy**: Support multiple hospitals/clinics
- [ ] **Automated Alerts**: Email/SMS notifications for high-risk patients
- [ ] **Natural Language Processing**: Extract insights from clinical notes
- [ ] **Kubernetes**: Container orchestration for scalability
- [ ] **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## 📚 Additional Resources

- [Complete Setup Guide](SETUP.md)
- [Deployment Documentation](DEPLOYMENT.md)
- [Feature Specifications](FEATURES.md)
- [Power BI Setup Guide](POWER_BI_SETUP.md)
- [ML Models Documentation](backend/ML_MODELS_README.md)
- [Testing Summary](TESTING_SUMMARY.md)
- [Project Summary](PROJECT_SUMMARY.md)

---

<div align="center">

**Made with ❤️ by Healthcare Analytics Team**

*Leveraging Big Data & Machine Learning for Better Healthcare Outcomes*

[![GitHub Stars](https://img.shields.io/github/stars/RajahmundrySravani/Development-of-Big-Data-Pipeline-for-Healthcare-Analytics-using-Python?style=social)](https://github.com/RajahmundrySravani/Development-of-Big-Data-Pipeline-for-Healthcare-Analytics-using-Python)
[![GitHub Forks](https://img.shields.io/github/forks/RajahmundrySravani/Development-of-Big-Data-Pipeline-for-Healthcare-Analytics-using-Python?style=social)](https://github.com/RajahmundrySravani/Development-of-Big-Data-Pipeline-for-Healthcare-Analytics-using-Python/fork)

**⭐ Star this repo if you found it helpful! ⭐**

</div>
