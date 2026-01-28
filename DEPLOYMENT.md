# Healthcare Analytics System - Deployment Guide

## 🌐 Deploy Frontend to Vercel (Get HTTPS URL)

### Method 1: Vercel Dashboard (Easiest)

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub, GitLab, or email

2. **Push Code to GitHub**
   ```bash
   # In your project root
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/healthcare-analytics.git
   git push -u origin main
   ```

3. **Import Project to Vercel**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Click "Deploy"

4. **Get Your URL**
   - Vercel automatically generates: `https://your-project.vercel.app`
   - Custom domain available in settings

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? healthcare-analytics
# - Directory? ./
# - Override settings? No

# Get production URL
vercel --prod
```

## 🚀 Deploy Backend Options

### Option 1: Render (Free, Easy)

1. Go to https://render.com
2. Sign up and create new Web Service
3. Connect GitHub repository
4. Settings:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables
6. Deploy!

### Option 2: Heroku

```bash
# Install Heroku CLI
# Create Procfile in backend/
echo "web: gunicorn app:app" > backend/Procfile

# Deploy
cd backend
heroku create healthcare-backend
git push heroku main
heroku config:set MONGO_URI=your_uri
```

### Option 3: AWS EC2

1. Launch EC2 instance (Ubuntu)
2. SSH into instance
3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   ```
4. Clone repository and run Flask
5. Configure Nginx as reverse proxy

## 🔧 Update Frontend API URL

After deploying backend, update frontend:

```env
# frontend/.env
REACT_APP_API_URL=https://your-backend-url.com/api
```

Redeploy frontend on Vercel.

## 📊 Full Deployment Checklist

- [ ] MongoDB Atlas setup (cloud database)
- [ ] AWS S3 bucket created
- [ ] Backend deployed and running
- [ ] Frontend deployed on Vercel
- [ ] API URL updated in frontend
- [ ] Environment variables configured
- [ ] HTTPS working
- [ ] CORS configured correctly
- [ ] Test all features

## 🌍 Recommended Stack for Free Deployment

- **Frontend**: Vercel (Free, HTTPS included)
- **Backend**: Render (Free tier available)
- **Database**: MongoDB Atlas (Free tier 512MB)
- **Storage**: AWS S3 (Free tier 5GB)

## 🎯 Final URLs

After deployment, you'll have:
- Frontend: `https://healthcare-analytics.vercel.app`
- Backend: `https://healthcare-backend.onrender.com`

## 🔒 Security for Production

1. **Environment Variables**
   - Never commit `.env` files
   - Use platform environment variable settings

2. **CORS Configuration**
   ```python
   # backend/app.py
   CORS(app, origins=['https://healthcare-analytics.vercel.app'])
   ```

3. **MongoDB Security**
   - Use MongoDB Atlas with IP whitelist
   - Strong passwords

4. **AWS Security**
   - Use IAM roles with minimal permissions
   - Enable S3 bucket encryption

## 📱 Mobile Responsive

Your app is already mobile-responsive! Test on:
- Desktop browsers
- Mobile browsers
- Tablets

## 🎉 You're Done!

Your healthcare analytics system is now live with a real HTTPS URL!

Share your link: `https://your-project.vercel.app`
