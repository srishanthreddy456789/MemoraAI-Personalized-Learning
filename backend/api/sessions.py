from fastapi import APIRouter
from db.database import cursor

router = APIRouter()

@router.get("/sessions")
def list_sessions():
    cursor.execute("SELECT id, title, created_at FROM sessions ORDER BY created_at DESC")
    return [
        {"id": i, "title": t, "created_at": c}
        for i, t, c in cursor.fetchall()
    ]