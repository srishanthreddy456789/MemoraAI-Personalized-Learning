import uuid
from ml.predictor import predict_weakness
from typing import Optional
from fastapi import APIRouter
from genai.teacher import teacher_reply
from db.database import cursor, conn

router = APIRouter()

@router.post("/chat")
def chat(session_id: Optional[str], message: str):
    if not session_id:
        session_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO sessions (id, title) VALUES (?, ?)",
            (session_id, message[:30])
        )

    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ?",
        (session_id,)
    )
    history = [{"role": r, "content": c} for r, c in cursor.fetchall()]

    weak_topics = []
    # temporary dummy features (UI will send real ones later)
    features = {
        "last_studied_days": 3,
        "revision_count": 1,
        "quiz_score": 0.4
    }

    weak_topics = predict_weakness(features)
    reply = teacher_reply(message, history, weak_topics)

    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, "student", message)
    )
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, "teacher", reply)
    )
    conn.commit()

    return {
        "session_id": session_id,
        "reply": reply
    }