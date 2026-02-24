from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from ..db.database import get_connection
import re
from fastapi import Depends
from ..utils.dependencies import get_current_user
router = APIRouter()

# ---------------- Request Schema ----------------

class QuizSubmitRequest(BaseModel):
    quiz_id: int
    user_answer: str


# ---------------- Text Normalization ----------------

def normalize(text: str):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


# ---------------- Intelligent Comparison ----------------

def is_answer_correct(user_answer: str, correct_answer: str) -> bool:
    ua = normalize(user_answer)
    ca = normalize(correct_answer)

    if ua == ca:
        return True

    if ua in ca or ca in ua:
        return True

    ua_tokens = set(ua.split())
    ca_tokens = set(ca.split())

    if not ca_tokens:
        return False

    overlap_ratio = len(ua_tokens & ca_tokens) / len(ca_tokens)

    return overlap_ratio >= 0.6


# ---------------- Mastery Update ----------------

def update_mastery(current_score: float, correct: bool) -> float:
    if correct:
        new_score = current_score + 0.05
    else:
        new_score = current_score - 0.03

    return max(0.0, min(1.0, new_score))


# ---------------- Endpoint ----------------

@router.post("/quiz/submit")
def submit_quiz(payload: QuizSubmitRequest, user_id: int = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT q.topic, q.correct_answer
            FROM quizzes q
            JOIN sessions s ON q.session_id = s.id
            WHERE q.id = ? AND s.user_id = ?
        """, (payload.quiz_id, user_id))
        quiz = cursor.fetchone()

        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        topic, correct_answer = quiz
        correct = is_answer_correct(payload.user_answer, correct_answer)

        cursor.execute("""
            INSERT INTO quiz_results (quiz_id, topic, user_answer, is_correct)
            VALUES (?, ?, ?, ?)
        """, (payload.quiz_id, topic, payload.user_answer, int(correct)))

        cursor.execute("""
            SELECT t.mastery_score, t.revision_count
            FROM topics t
            JOIN sessions s ON t.session_id = s.id
            JOIN quizzes q ON q.session_id = s.id
            WHERE q.id = ? AND s.user_id = ?
        """, (payload.quiz_id, user_id))
        topic_data = cursor.fetchone()

        if not topic_data:
            raise HTTPException(status_code=404, detail="Topic not found")

        mastery_score, revision_count = topic_data

        new_mastery = update_mastery(mastery_score, correct)
        new_revision_count = revision_count + 1
        now = datetime.utcnow()

        cursor.execute("""
            UPDATE topics
            SET mastery_score = ?,
                revision_count = ?,
                last_reviewed = ?
            WHERE id = (
                SELECT t.id
                FROM topics t
                JOIN sessions s ON t.session_id = s.id
                JOIN quizzes q ON q.session_id = s.id
                WHERE q.id = ? AND s.user_id = ?
                LIMIT 1
            )
        """, (new_mastery, new_revision_count, now, payload.quiz_id, user_id))

        conn.commit()

        feedback = (
            "✅ Correct! Your mastery improved."
            if correct
            else f"❌ Not quite. Correct answer: {correct_answer}"
        )

        return {
            "is_correct": correct,
            "mastery_score": new_mastery,
            "revision_count": new_revision_count,
            "feedback": feedback
        }

    finally:
        cursor.close()
        conn.close()