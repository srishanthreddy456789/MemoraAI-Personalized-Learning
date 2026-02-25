from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 🔥 ADD THIS

from .api.chat import router as chat_router
from .api.sessions import router as sessions_router
from .api.predict import router as predict_router
from .api.quiz import router as quiz_router
from .api.auth import router as auth_router
from .db.database import init_db

app = FastAPI(title="MemoraAI Backend")

# 🔥 ADD THIS BLOCK RIGHT AFTER app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://memora-ai-personalized-learning.vercel.app",
        "https://memora-ai-personalized-learning-4753n08wa.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# 🔐 Auth must be included
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(predict_router)
app.include_router(quiz_router)

@app.get("/")
def health():
    return {"status": "Backend running"}