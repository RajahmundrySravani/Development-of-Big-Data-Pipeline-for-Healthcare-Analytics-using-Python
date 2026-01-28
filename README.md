# Healthcare Analytics System

A professional Healthcare Data Analytics System built with React, Flask, MongoDB, AWS S3, and PySpark.

## 🌟 Features

- **CSV Data Upload**: Upload patient, visit, and prescription CSV files
- **Real-time Data Entry**: Forms for entering healthcare data
- **Interactive Dashboard**: Visualize insights with charts and analytics
- **Cloud Integration**: AWS S3 for data storage
- **Data Processing**: PySpark for cleaning and aggregation
- **Professional UI**: Clean, responsive healthcare-themed interface

## 🏗️ Architecture

```
Data Sources → Frontend (React) → Backend (Flask) → MongoDB → AWS S3 → PySpark → Dashboard
```

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- MongoDB
- AWS Account (optional, for S3)

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on: http://localhost:3000

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs on: http://localhost:5000

## 📁 Project Structure

```
sun_healthcare_final/
├── frontend/                 # React application
│   ├── public/
│   ├── src/
│   │   ├── components/      # Navbar, etc.
│   │   ├── pages/           # Home, Upload, DataEntry, Dashboard
│   │   ├── services/        # API service layer
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── backend/                  # Flask API server
│   ├── app.py               # Main backend application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
│
└── README.md
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

1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to frontend: `cd frontend`
3. Deploy: `vercel`
4. Follow prompts and get your live URL!

### Deploy Backend

Options:
- **AWS EC2**: Traditional server hosting
- **Heroku**: Simple deployment platform
- **AWS Lambda**: Serverless deployment
- **DigitalOcean**: Droplet hosting

## 📊 API Endpoints

### Upload
- `POST /api/upload` - Upload CSV file

### Patients
- `POST /api/patient` - Create patient
- `GET /api/patients` - Get all patients

### Visits
- `POST /api/visit` - Create visit
- `GET /api/visits` - Get all visits

### Prescriptions
- `POST /api/prescription` - Create prescription
- `GET /api/prescriptions` - Get all prescriptions

### Analytics
- `GET /api/dashboard` - Get dashboard data
- `GET /api/health` - Health check

## 🎨 Tech Stack

### Frontend
- React 18
- React Router 6
- Recharts (visualizations)
- Axios (API calls)
- React Icons

### Backend
- Flask 3.0
- PyMongo
- Boto3 (AWS SDK)
- Flask-CORS

### Infrastructure
- MongoDB (database)
- AWS S3 (data lake)
- PySpark (data processing)

## 📝 Usage Guide

### 1. Upload CSV Files
- Navigate to "Upload Data"
- Select CSV files for patients, visits, or prescriptions
- Click upload to store in S3

### 2. Enter Data via Forms
- Go to "Data Entry"
- Fill patient, visit, or prescription forms
- Data saved to MongoDB

### 3. View Analytics
- Open "Dashboard"
- See charts and statistics
- Download reports

## 🔒 Security Notes

- Never commit `.env` files
- Keep AWS credentials secure
- Use environment variables for sensitive data
- Enable CORS only for trusted origins in production

## 📄 License

This project is for educational purposes.

## 👥 Contributors

Healthcare Analytics Team

## 📞 Support

For issues or questions, please create an issue in the repository.

---

Made with ❤️ for Healthcare Analytics
