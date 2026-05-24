<div align="center">

# 🧠 MemoraAI — Personalized Learning Assistant

**An adaptive AI-powered tutor that learns with you.**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Visit_App-7c3aed?style=for-the-badge)](https://memora-ai-personalized-learning.vercel.app/)
[![Backend](https://img.shields.io/badge/⚡_Backend-Render-00d68f?style=for-the-badge)](https://memoraai-personalized-learning.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/srishanthreddy456789/MemoraAI-Personalized-Learning)

</div>

---

## 🌐 Live Deployment

| Service | URL |
|---------|-----|
| 🖥️ **Frontend** | [https://memora-ai-personalized-learning.vercel.app](https://memora-ai-personalized-learning.vercel.app/) |
| ⚙️ **Backend API** | [https://memoraai-personalized-learning.onrender.com](https://memoraai-personalized-learning.onrender.com) |
| 📖 **API Docs** | [https://memoraai-personalized-learning.onrender.com/docs](https://memoraai-personalized-learning.onrender.com/docs) |

---

## ✨ Features

- 🤖 **AI-Powered Chat** — Adaptive tutor powered by Groq (Llama 3.3 70B)
- 📚 **Personalized Learning** — Tracks your weak topics and adjusts difficulty
- 🧪 **Quiz Generation** — Auto-generates MCQ quizzes based on your mastery level
- 📈 **Forgetting Curve** — Uses Ebbinghaus spaced repetition to schedule revisions
- 🔐 **JWT Authentication** — Secure login/register with token-based auth
- 💾 **Session History** — All your conversations are saved and searchable
- 🌙 **Dark/Light Mode** — Toggle between themes
- 📱 **Responsive Design** — Works on desktop and mobile

---

## 🏗️ Architecture

```
Frontend (React + Vite)          Backend (FastAPI + Python)
┌─────────────────────┐          ┌──────────────────────────┐
│  Vercel (CDN)       │  HTTPS   │  Render (Web Service)    │
│                     │ ──────── │                          │
│  React + TypeScript │          │  FastAPI REST API        │
│  React Router       │          │  SQLite Database         │
│  TailwindCSS        │          │  JWT Authentication      │
│  ShadCN UI          │          │  Groq LLM (Llama 3.3)    │
│                     │          │  Scikit-learn ML         │
└─────────────────────┘          └──────────────────────────┘
```

---

## 🚀 Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| React 18 + TypeScript | UI framework |
| Vite | Build tool |
| React Router v6 | Client-side routing |
| TailwindCSS | Styling |
| ShadCN UI | Component library |
| Lucide React | Icons |

### Backend
| Technology | Purpose |
|-----------|---------|
| FastAPI | REST API framework |
| SQLite | Database (sessions, messages, topics) |
| python-jose | JWT authentication |
| passlib + bcrypt | Password hashing |
| Groq SDK | AI chat (Llama 3.3 70B) |
| Scikit-learn | Topic weakness prediction |

---

## 🛠️ Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/srishanthreddy456789/MemoraAI-Personalized-Learning.git
cd MemoraAI-Personalized-Learning
```

### 2. Setup Backend
```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_groq_key_here" > .env
echo "JWT_SECRET_KEY=your_secret_here" >> .env
echo "ALLOWED_ORIGINS=http://localhost:5173" >> .env

# Run the server
uvicorn backend.main:app --reload
```
Backend will be available at `http://localhost:8000`

### 3. Setup Frontend
```bash
cd frontend

# Create .env.local
echo "VITE_API_BASE_URL=http://localhost:8000" > .env.local

# Install and run
npm install
npm run dev
```
Frontend will be available at `http://localhost:5173`

---

## 🌍 Deployment

### Frontend — Vercel
Set this environment variable in Vercel Dashboard → Settings → Environment Variables:

| Variable | Value |
|----------|-------|
| `VITE_API_BASE_URL` | `https://memoraai-personalized-learning.onrender.com` |

### Backend — Render
Set these environment variables in Render Dashboard → Environment:

| Variable | Value |
|----------|-------|
| `GROQ_API_KEY` | Your Groq API key (free at [console.groq.com](https://console.groq.com)) |
| `JWT_SECRET_KEY` | A long random secret string |
| `ALLOWED_ORIGINS` | `https://memora-ai-personalized-learning.vercel.app` |

**Start Command:**
```
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

---

## 📁 Project Structure

```
MemoraAI-Personalized-Learning/
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Index.tsx       # Main chat interface
│   │   │   ├── Login.tsx       # Login page
│   │   │   └── register.tsx    # Registration page
│   │   ├── lib/
│   │   │   └── api.ts          # Centralized API config
│   │   └── components/         # UI components
│   ├── .env.example            # Environment template
│   └── vercel.json             # Vercel configuration
│
├── backend/                    # FastAPI backend
│   ├── api/
│   │   ├── auth.py             # Login/Register endpoints
│   │   ├── chat.py             # Chat endpoint
│   │   ├── sessions.py         # Session management
│   │   ├── quiz.py             # Quiz generation
│   │   └── predict.py          # Weakness prediction
│   ├── db/
│   │   └── database.py         # SQLite schema + connection
│   ├── genai/
│   │   ├── teacher.py          # Groq LLM integration
│   │   └── prompts.py          # System prompts
│   ├── ml/
│   │   └── predictor.py        # ML weakness predictor
│   ├── utils/
│   │   └── dependencies.py     # JWT auth dependency
│   ├── .env.example            # Environment template
│   └── requirements.txt        # Python dependencies
│
├── render.yaml                 # Render deployment config
└── README.md
```

---

## 🔑 Environment Variables

### Frontend (`.env.local`)
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Backend (`.env`)
```env
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_jwt_secret_key
ALLOWED_ORIGINS=http://localhost:5173
```

---

## 📄 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Create account | No |
| POST | `/login` | Get JWT token | No |
| GET | `/health` | Health check | No |
| POST | `/chat` | Send message to AI | Yes |
| GET | `/sessions` | List chat sessions | Yes |
| DELETE | `/sessions/{id}` | Delete a session | Yes |
| POST | `/quiz` | Generate quiz | Yes |
| POST | `/predict` | Predict weakness | Yes |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ by [srishanthreddy456789](https://github.com/srishanthreddy456789)

⭐ **Star this repo if you found it helpful!**

</div>
