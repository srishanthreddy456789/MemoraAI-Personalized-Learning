import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.chat import router as chat_router
from .api.sessions import router as sessions_router
from .api.predict import router as predict_router
from .api.quiz import router as quiz_router
from .api.auth import router as auth_router
from .db.database import init_db

app = FastAPI(title="MemoraAI Backend")

# ✅ FIXED: Proper CORS configuration for production
# Reads allowed origins from environment variable or uses defaults
_raw_origins = os.environ.get(
    "ALLOWED_ORIGINS",
    "https://memora-ai-personalized-learning.vercel.app,http://localhost:5173,http://localhost:8080,http://127.0.0.1:5173"
)
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(predict_router)
app.include_router(quiz_router)


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/health")
async def health_check():
    """Health check endpoint for frontend auth guard and Render health checks."""
    return {"status": "ok", "service": "MemoraAI Backend"}


if __name__ == "__main__":
    import uvicorn

    # ✅ FIXED: Bind to 0.0.0.0 and use dynamic PORT env variable for Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=False)
