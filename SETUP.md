# 🚀 Quick Setup Guide - Healthcare Analytics System

## Step 1: Install Frontend Dependencies

Open PowerShell/Terminal and run:

```powershell
cd d:\moon\BigData\sun_healthcare_final\frontend
npm install
```

This installs all React dependencies (React Router, Recharts, Axios, etc.)

---

## Step 2: Install Backend Dependencies

Open a **new** terminal window:

```powershell
cd d:\moon\BigData\sun_healthcare_final\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

# Install Python packages
pip install -r requirements.txt
```

---

## Step 3: Configure Environment Variables

### Backend Configuration

1. Copy `.env.example` to `.env` in backend folder:
   ```powershell
   cd d:\moon\BigData\sun_healthcare_final\backend
   copy .env.example .env
   ```

2. Edit `.env` file with your credentials:
   ```env
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DB=healthcare_analytics
   AWS_ACCESS_KEY_ID=your_actual_aws_key
   AWS_SECRET_ACCESS_KEY=your_actual_aws_secret
   AWS_BUCKET_NAME=your-bucket-name
   AWS_REGION=us-east-1
   ```

**Note**: MongoDB and AWS are optional for initial testing!

---

## Step 4: Start the Backend Server

```powershell
cd d:\moon\BigData\sun_healthcare_final\backend
.\venv\Scripts\activate  # If not already activated
python app.py
```

You should see:
```
🚀 Starting Healthcare Analytics Backend Server...
📊 MongoDB: ✅ Connected (or ❌ Not connected)
☁️  AWS S3: ✅ Connected (or ❌ Not connected)
```

Backend runs on: **http://localhost:5000**

---

## Step 5: Start the Frontend

Open **another** terminal window:

```powershell
cd d:\moon\BigData\sun_healthcare_final\frontend
npm start
```

Browser automatically opens to: **http://localhost:3000**

---

## ✅ You're Ready!

Your application is now running locally:

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

### Test the Application:

1. **Home Page**: See project overview
2. **Upload Data**: Upload CSV files (works even without S3)
3. **Data Entry**: Fill forms to add patient/visit/prescription data
4. **Dashboard**: View beautiful analytics charts

---

## 🌐 Deploy to Get HTTPS URL

When ready to deploy and get a real URL:

```powershell
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd d:\moon\BigData\sun_healthcare_final\frontend
vercel

# Follow prompts, and you'll get: https://your-project.vercel.app
```

Full deployment guide: See `DEPLOYMENT.md`

---

## 🔧 Troubleshooting

### Port Already in Use?

**Frontend (3000)**:
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

**Backend (5000)**:
```powershell
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### MongoDB Not Installed?

That's okay! The app will work without MongoDB for now. Data won't persist, but all features will display.

To install MongoDB:
- Download from: https://www.mongodb.com/try/download/community
- Or use MongoDB Atlas (free cloud): https://www.mongodb.com/cloud/atlas

### AWS S3 Not Configured?

Also okay! Files will be saved locally in `backend/uploads/` folder. You can configure S3 later.

---

## 📂 Project Structure

```
sun_healthcare_final/
├── frontend/           ← React application
│   ├── src/
│   │   ├── components/  ← Navbar
│   │   ├── pages/       ← Home, Upload, DataEntry, Dashboard
│   │   └── services/    ← API calls
│   └── package.json
│
├── backend/            ← Flask API
│   ├── app.py          ← Main server file
│   └── requirements.txt
│
├── README.md           ← Full documentation
└── DEPLOYMENT.md       ← Deployment instructions
```

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Start backend server
3. ✅ Start frontend application
4. ✅ Test all features locally
5. 🚀 Deploy to Vercel for HTTPS URL
6. 🎉 Share your live website!

---

## 💡 Need Help?

Check these files:
- `README.md` - Complete documentation
- `DEPLOYMENT.md` - Step-by-step deployment guide

---

**You're all set! Start building your Healthcare Analytics System! 🏥📊**
