from fastapi import APIRouter, Depends, HTTPException
from ..db.database import get_connection
from ..utils.dependencies import get_current_user

router = APIRouter()


# 🔹 Get all sessions for logged-in user
@router.get("/sessions")
def list_sessions(user_id: int = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, title, created_at FROM sessions WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        )

        sessions = [
            {"id": i, "title": t, "created_at": c}
            for i, t, c in cursor.fetchall()
        ]

        return sessions

    finally:
        cursor.close()
        conn.close()


# 🔹 Get full chat history for one session
@router.get("/sessions/{session_id}")
def get_session(session_id: str, user_id: int = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Verify session belongs to user
        cursor.execute(
            "SELECT id FROM sessions WHERE id=? AND user_id=?",
            (session_id, user_id)
        )

        if not cursor.fetchone():
            raise HTTPException(status_code=403, detail="Unauthorized session")

        # Fetch messages
        cursor.execute(
            """SELECT role, content
               FROM messages
               WHERE session_id=?
               ORDER BY created_at ASC""",
            (session_id,)
        )

        messages = [
            {"role": r, "content": c}
            for r, c in cursor.fetchall()
        ]

        return messages

    finally:
        cursor.close()
        conn.close()