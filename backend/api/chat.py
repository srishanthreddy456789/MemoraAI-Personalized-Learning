import uuid
import math
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..ml.predictor import predict_weakness
from ..genai.teacher import teacher_reply, extract_topic
from ..db.database import get_connection
from ..utils.dependencies import get_current_user

router = APIRouter()


def forgetting_probability(days_since: float, mastery_score: float, revision_count: int) -> float:
    """Ebbinghaus-inspired forgetting curve with mastery adjustment."""
    decay_rate = 0.1 + (0.2 * (1 - mastery_score))
    stability = max(0.5, revision_count * mastery_score)
    time_decay = math.exp(-decay_rate * days_since / stability)
    adaptive_factor = (1 - mastery_score)
    return time_decay * adaptive_factor


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str


@router.post("/chat")
def chat(request: ChatRequest, user_id: int = Depends(get_current_user)):
    """Handle a chat message from the student."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        session_id = request.session_id

        # ---------- Create new session if needed ----------
        if not session_id:
            session_id = str(uuid.uuid4())
            title = request.message[:40].strip()
            cursor.execute(
                "INSERT INTO sessions (id, user_id, title) VALUES (?, ?, ?)",
                (session_id, user_id, title)
            )
            conn.commit()
        else:
            # Verify session ownership
            cursor.execute(
                "SELECT id FROM sessions WHERE id=? AND user_id=?",
                (session_id, user_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=403, detail="Unauthorized session access")

        # ---------- Fetch chat history ----------
        cursor.execute(
            "SELECT role, content FROM messages WHERE session_id=? ORDER BY created_at ASC",
            (session_id,)
        )
        history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

        # ---------- Get weak topics ----------
        cursor.execute(
            "SELECT topic FROM topics WHERE session_id=? AND mastery_score < 0.5",
            (session_id,)
        )
        weak_topics = [row[0] for row in cursor.fetchall()]

        # ---------- Generate AI reply ----------
        reply = teacher_reply(request.message, history, weak_topics)

        # ---------- Save messages ----------
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, "student", request.message)
        )
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, "teacher", reply)
        )

        # ---------- Update topic mastery ----------
        topic = extract_topic(request.message)
        cursor.execute(
            "SELECT id, mastery_score, revision_count FROM topics WHERE session_id=? AND topic=?",
            (session_id, topic)
        )
        existing = cursor.fetchone()

        if existing:
            topic_id, mastery, revisions = existing
            # Predict whether this is still a weakness
            features = {
                "last_studied_days": 0,
                "revision_count": revisions + 1,
                "quiz_score": mastery
            }
            is_weak = predict_weakness(features)[0] == 1
            new_mastery = max(0.1, mastery + (0.05 if not is_weak else -0.02))

            cursor.execute(
                """UPDATE topics SET mastery_score=?, revision_count=?, last_revised=?
                   WHERE id=?""",
                (new_mastery, revisions + 1, datetime.utcnow(), topic_id)
            )
        else:
            cursor.execute(
                "INSERT INTO topics (session_id, topic, mastery_score, revision_count) VALUES (?, ?, ?, ?)",
                (session_id, topic, 0.5, 1)
            )

        conn.commit()

        return {
            "reply": reply,
            "session_id": session_id,
            "topic": topic
        }

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
    finally:
        cursor.close()
        conn.close()