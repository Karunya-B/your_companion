# 🤖 Your Companion

A personal AI mentor and life orchestrator built with FastAPI and React.

## ✨ Features

- **AI Chat Partner**: Talk to your personal AI mentor who remembers your conversation history
- **Task Planning**: Get AI-generated study plans based on your goals and energy levels
- **Daily Guidance**: Receive personalized guidance based on your mood, sleep, and workload
- **Progress Tracking**: Log tasks, health metrics, screen time, and reflections
- **Smart Learning**: AI learns your preferences and adapts to your learning style

## 🚀 Live Deployment

Your app is deployed and live on **Railway**! 

- **GitHub Repository**: [Karunya-B/your_companion](https://github.com/Karunya-B/your_companion)
- **Deployed via**: GitHub + Railway (auto-deploys on push)
- **Configuration**: See `railway.json` for deployment spec

## 🏗️ Tech Stack

- **Backend**: FastAPI + SQLAlchemy + Groq API
- **Frontend**: React + Vite
- **Database**: SQLite
- **Deployment**: Railway (Docker)
- **AI Model**: Groq (llama-3.3-70b-versatile)

## 📦 Local Development

```bash
# Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

### Environment Variables (Backend)
```
GROQ_API_KEY=your_groq_api_key_here
```

Add via Railway Dashboard → Variables tab

## 📚 API Documentation

- **Interactive Docs**: `/docs` (Swagger UI)
- **Base URL**: Your Railway backend URL
- **Main Endpoints**:
  - `POST /api/v1/chat` - Send a chat message
  - `GET /api/v1/generate_daily_guidance` - Get daily guidance
  - `POST /api/v1/log_daily_tasks` - Log tasks
  - `GET /api/v1/chat/history` - Get chat history

## 🧪 Testing

1. Visit your deployed frontend URL
2. Send a chat message
3. Verify AI remembers conversation context
4. Check task logging and data persistence

## 📝 License

Open source project