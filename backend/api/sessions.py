from fastapi import APIRouter, Depends, HTTPException
from ..db.database import get_connection
from ..utils.dependencies import get_current_user

router = APIRouter()


# ✅ Get all sessions for the logged-in user
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
            {"id": row[0], "title": row[1], "created_at": row[2]}
            for row in cursor.fetchall()
        ]
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")
    finally:
        cursor.close()
        conn.close()


# ✅ Delete a session (and its messages)
@router.delete("/sessions/{session_id}")
def delete_session(session_id: str, user_id: int = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verify ownership
        cursor.execute(
            "SELECT id FROM sessions WHERE id=? AND user_id=?",
            (session_id, user_id)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=403, detail="Unauthorized session access")

        # Delete messages first (FK constraint)
        cursor.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
        cursor.execute("DELETE FROM topics WHERE session_id=?", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE id=?", (session_id,))
        conn.commit()
        return {"message": "Session deleted"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")
    finally:
        cursor.close()
        conn.close()