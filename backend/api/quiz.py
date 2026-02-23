from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from ..db.database import conn, cursor
import re

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
def submit_quiz(payload: QuizSubmitRequest):

    # Fetch quiz
    cursor.execute(
        "SELECT topic, correct_answer FROM quizzes WHERE id = ?",
        (payload.quiz_id,)
    )
    quiz = cursor.fetchone()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    topic, correct_answer = quiz

    # Check correctness
    correct = is_answer_correct(payload.user_answer, correct_answer)

    # Save result
    cursor.execute("""
        INSERT INTO quiz_results (quiz_id, topic, user_answer, is_correct)
        VALUES (?, ?, ?, ?)
    """, (payload.quiz_id, topic, payload.user_answer, int(correct)))

    # Fetch topic mastery
    cursor.execute("""
        SELECT mastery_score, revision_count
        FROM topics
        WHERE topic = ?
    """, (topic,))
    topic_data = cursor.fetchone()

    if not topic_data:
        raise HTTPException(status_code=404, detail="Topic not found")

    mastery_score, revision_count = topic_data

    # Update mastery
    new_mastery = update_mastery(mastery_score, correct)
    new_revision_count = revision_count + 1
    now = datetime.utcnow()

    cursor.execute("""
        UPDATE topics
        SET mastery_score = ?,
            revision_count = ?,
            last_reviewed = ?
        WHERE topic = ?
    """, (new_mastery, new_revision_count, now, topic))

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