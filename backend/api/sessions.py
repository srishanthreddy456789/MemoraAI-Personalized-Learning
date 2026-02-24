from fastapi import APIRouter
from ..db.database import get_connection

router = APIRouter()

@router.get("/sessions")
def list_sessions():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, title, created_at FROM sessions ORDER BY created_at DESC"
        )
        sessions = [
            {"id": i, "title": t, "created_at": c}
            for i, t, c in cursor.fetchall()
        ]
        return sessions

    finally:
        cursor.close()
        conn.close()