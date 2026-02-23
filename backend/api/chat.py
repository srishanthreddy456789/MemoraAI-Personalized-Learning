import uuid
from typing import Optional
from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from ..ml.predictor import predict_weakness
from ..genai.teacher import teacher_reply
from ..db.database import cursor, conn
import math

def forgetting_probability(days_since, mastery_score, revision_count):

    # Dynamic decay: weak topics decay faster
    decay_rate = 0.1 + (0.2 * (1 - mastery_score))

    # Stability floor
    stability = max(0.5, revision_count * mastery_score)

    # Time decay
    time_decay = math.exp(-decay_rate * days_since)

    # Mastery reduces forgetting risk
    adaptive_factor = (1 - mastery_score)

    return time_decay * adaptive_factor

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

@router.post("/quiz")
def quiz(request: ChatRequest):

    from ..genai.teacher import generate_quiz, extract_topic

    topic = extract_topic(request.message)

    # Fetch mastery for this topic
    cursor.execute(
        "SELECT mastery_score FROM topics WHERE session_id=? AND topic=?",
        (request.session_id, topic)
    )
    row = cursor.fetchone()
    mastery = row[0] if row else 0.5

    question, answer = generate_quiz(topic, mastery)

    cursor.execute(
        "INSERT INTO quizzes (session_id, topic, question, correct_answer) VALUES (?, ?, ?, ?)",
        (request.session_id, topic, question, answer)
    )

    conn.commit()

    return {
        "session_id": request.session_id,
        "quiz": question
    }

    cursor.execute(
        "INSERT INTO quizzes (session_id, topic, question, correct_answer) VALUES (?, ?, ?, ?)",
        (request.session_id, topic, quiz_text, "")
    )
    conn.commit()

    return {
        "session_id": request.session_id,
        "quiz": quiz_text
    }
@router.post("/chat")
def chat(request: ChatRequest):

    session_id = request.session_id
    message = request.message

    # -----------------------------
    # Create session if not exists
    # -----------------------------
    if not session_id:
        session_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO sessions (id, title) VALUES (?, ?)",
            (session_id, message[:30])
        )

    # -----------------------------
    # Get previous chat history
    # -----------------------------
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ?",
        (session_id,)
    )
    history = [{"role": r, "content": c} for r, c in cursor.fetchall()]

    # -----------------------------
    # Topic Tracking Logic
    # -----------------------------
    from ..genai.teacher import extract_topic
    topic = extract_topic(message)

    cursor.execute(
    "SELECT revision_count, last_reviewed, mastery_score FROM topics WHERE session_id=? AND topic=?",
    (session_id, topic)
    )

    row = cursor.fetchone()

    if row:
        revision_count, last_reviewed, mastery_score = row
        last_reviewed = datetime.fromisoformat(last_reviewed)

        cursor.execute(
            """UPDATE topics 
            SET revision_count = revision_count + 1,
                last_reviewed = CURRENT_TIMESTAMP
            WHERE session_id=? AND topic=?""",
            (session_id, topic)
        )

    else:
        revision_count = 1
        mastery_score = 0.5
        last_reviewed = datetime.now()

        cursor.execute(
            "INSERT INTO topics (session_id, topic) VALUES (?, ?)",
            (session_id, topic)
        )

    conn.commit()

    # -----------------------------
    # Build Real ML Features
    # -----------------------------
    days_since = (datetime.now() - last_reviewed).days
    forget_prob = forgetting_probability(days_since, mastery_score, revision_count)

    features = {
        "last_studied_days": days_since,
        "revision_count": revision_count,
        "quiz_score": 0.5  # temporary until quiz system added
    }

    # -----------------------------
    # ML Prediction
    # -----------------------------
    weak_topics = predict_weakness(features)
    from ..genai.teacher import generate_quiz

    auto_quiz = None

    # If forgetting probability is LOW → high forgetting risk
    if forget_prob < 0.4:
        question, answer = generate_quiz(topic, mastery_score)

        cursor.execute(
            "INSERT INTO quizzes (session_id, topic, question, correct_answer) VALUES (?, ?, ?, ?)",
            (session_id, topic, question, answer)
        )

        auto_quiz = question
        conn.commit()

    # -----------------------------
    # GenAI Response
    # -----------------------------
    reply = teacher_reply(message, history, weak_topics)

    # -----------------------------
    # Save Messages
    # -----------------------------
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
        "reply": reply,
        "weak_topics": weak_topics,
        "auto_quiz": auto_quiz,
        "forgetting_probability": forget_prob
    }