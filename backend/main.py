from fastapi import FastAPI
from .api.chat import router as chat_router
from .api.sessions import router as sessions_router
from .api.predict import router as predict_router
from .api.quiz import router as quiz_router   # 👈 ADD THIS
from .db.database import init_db

app = FastAPI(title="MemoraAI Backend")

init_db()
print("Initializing DB...")
app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(predict_router)
app.include_router(quiz_router)   # 👈 ADD THIS


@app.get("/")
def health():
    return {"status": "Backend running"}