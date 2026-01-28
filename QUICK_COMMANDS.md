# ⚡ Quick Commands Reference - Healthcare Analytics

## 🚀 First Time Setup

### Install Frontend Dependencies
```powershell
cd d:\moon\BigData\sun_healthcare_final\frontend
npm install
```

### Install Backend Dependencies
```powershell
cd d:\moon\BigData\sun_healthcare_final\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏃 Run Application (Every Time)

### Start Backend (Terminal 1)
```powershell
cd d:\moon\BigData\sun_healthcare_final\backend
.\venv\Scripts\activate
python app.py
```
**Backend runs on:** http://localhost:5000

### Start Frontend (Terminal 2)
```powershell
cd d:\moon\BigData\sun_healthcare_final\frontend
npm start
```
**Frontend opens:** http://localhost:3000

---

## 🌐 Deploy to Get HTTPS URL

### Deploy Frontend to Vercel
```powershell
# Install Vercel CLI (one time)
npm install -g vercel

# Deploy
cd d:\moon\BigData\sun_healthcare_final\frontend
vercel

# Production deployment
vercel --prod
```
**You get:** https://your-project.vercel.app

---

## 🔧 Useful Commands

### Frontend Commands
```powershell
# Navigate to frontend
cd d:\moon\BigData\sun_healthcare_final\frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Backend Commands
```powershell
# Navigate to backend
cd d:\moon\BigData\sun_healthcare_final\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Deactivate virtual environment
deactivate
```

---

## 🛠️ Troubleshooting Commands

### Kill Process on Port 3000
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

### Kill Process on Port 5000
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Clear Node Modules and Reinstall
```powershell
cd d:\moon\BigData\sun_healthcare_final\frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Recreate Python Virtual Environment
```powershell
cd d:\moon\BigData\sun_healthcare_final\backend
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📦 Install Optional Services

### Install MongoDB (Windows)
```powershell
# Download from: https://www.mongodb.com/try/download/community
# Or use chocolatey:
choco install mongodb

# Start MongoDB
mongod
```

### MongoDB Atlas (Cloud - Free)
1. Go to: https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update backend/.env with connection string

---

## 🔐 Environment Variables

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

---

## 📊 Project Structure Navigation

```powershell
# Go to project root
cd d:\moon\BigData\sun_healthcare_final

# Frontend
cd frontend

# Backend
cd backend

# View frontend components
cd frontend\src\components

# View frontend pages
cd frontend\src\pages

# View backend uploads
cd backend\uploads
```

---

## 🧪 Test API Endpoints

### Using PowerShell (curl)
```powershell
# Health check
curl http://localhost:5000/api/health

# Get dashboard data
curl http://localhost:5000/api/dashboard

# Create patient
curl -X POST http://localhost:5000/api/patient `
  -H "Content-Type: application/json" `
  -d '{\"name\":\"John Doe\",\"age\":30,\"gender\":\"Male\"}'
```

---

## 🎨 Customize Application

### Change Primary Color
Edit: `frontend\src\index.css`
```css
/* Change #2563eb to your color */
```

### Change App Title
Edit: `frontend\public\index.html`
```html
<title>Your Custom Title</title>
```

### Add New Page
1. Create `frontend\src\pages\NewPage.js`
2. Create `frontend\src\pages\NewPage.css`
3. Add route in `frontend\src\App.js`
4. Add link in `frontend\src\components\Navbar.js`

---

## 📝 Git Commands (If Using Version Control)

```powershell
# Initialize git
cd d:\moon\BigData\sun_healthcare_final
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote
git remote add origin https://github.com/yourusername/healthcare-analytics.git

# Push
git push -u origin main
```

---

## 🎯 Quick Links

- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Backend Health: http://localhost:5000/api/health
- Backend Dashboard: http://localhost:5000/api/dashboard

---

## ⚡ One-Line Quick Start

```powershell
# Open two terminals and run these:

# Terminal 1:
cd d:\moon\BigData\sun_healthcare_final\backend && .\venv\Scripts\activate && python app.py

# Terminal 2:
cd d:\moon\BigData\sun_healthcare_final\frontend && npm start
```

---

## 📚 Documentation Files

- `README.md` - Complete overview
- `SETUP.md` - Setup guide
- `DEPLOYMENT.md` - Deployment guide
- `FEATURES.md` - Features list
- `PROJECT_SUMMARY.md` - Project summary
- `QUICK_COMMANDS.md` - This file

---

**Save this file for quick reference! 📌**
