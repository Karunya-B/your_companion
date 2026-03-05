# Karunya Companion - Deployment Guide

A personal AI mentor and life orchestrator built with FastAPI and React.

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Full Stack)

Railway is perfect for full-stack apps with databases.

1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up
2. **Connect GitHub**: Link your GitHub repository
3. **Deploy Backend**:
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway will auto-detect Python and install dependencies
   - Add environment variables in Railway dashboard:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
4. **Deploy Frontend**:
   - Create another project for the frontend
   - Set build command: `npm run build`
   - Set publish directory: `dist`
   - Add environment variable: `VITE_API_URL=https://your-backend-url.up.railway.app/api/v1`

### Option 2: Render (Free Tier Available)

1. **Create Render Account**: Go to [render.com](https://render.com)
2. **Deploy Backend**:
   - New → Web Service → Connect GitHub
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables
3. **Deploy Frontend**:
   - New → Static Site → Connect GitHub
   - Build Command: `npm run build`
   - Publish Directory: `dist`
   - Add environment variable: `VITE_API_URL=https://your-backend.onrender.com/api/v1`

### Option 3: Vercel + Railway

1. **Deploy Backend on Railway** (as above)
2. **Deploy Frontend on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repo
   - Set root directory to `frontend`
   - Add environment variable: `VITE_API_URL=https://your-railway-backend.up.railway.app/api/v1`

## 🐳 Docker Deployment

### Local Development
```bash
# Build and run with docker-compose
docker-compose up --build
```

### Production Docker
```bash
# Build backend
docker build -t karunya-backend .

# Run backend
docker run -p 8000:8000 -e GROQ_API_KEY=your_key karunya-backend

# Build frontend
cd frontend
docker build -f ../Dockerfile.frontend -t karunya-frontend .
docker run -p 80:80 karunya-frontend
```

## 🔧 Environment Variables

### Backend (.env)
```
GROQ_API_KEY=your_groq_api_key_here
```

### Frontend (.env.production)
```
VITE_API_URL=https://your-backend-url.com/api/v1
```

## 🌐 Domain Setup

1. **Railway**: Custom domains available in paid plans
2. **Render**: Free custom domains
3. **Vercel**: Free custom domains with automatic HTTPS

## 📊 Database

- Uses SQLite (file-based)
- Automatically created on first run
- Data persists between deployments on Railway/Render

## 🔒 Security Notes

- CORS is configured for production
- API keys are stored as environment variables
- SQLite database is suitable for single-user apps

## 🚀 URLs After Deployment

- **Backend API**: `https://your-backend-url.com/api/v1`
- **Frontend**: `https://your-frontend-url.com`
- **API Docs**: `https://your-backend-url.com/docs`

## 🧪 Testing Deployment

1. Visit your frontend URL
2. Try sending a chat message
3. Check browser console for API errors
4. Verify data persists between sessions