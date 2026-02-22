from fastapi import FastAPI
from api.chat import router as chat_router
from api.sessions import router as sessions_router
from db.database import init_db

app = FastAPI(title="MemoraAI Backend")

init_db()

app.include_router(chat_router)
app.include_router(sessions_router)

@app.get("/")
def health():
    return {"status": "Backend running"}