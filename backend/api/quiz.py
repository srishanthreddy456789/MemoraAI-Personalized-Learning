from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..db.database import get_connection
from ..genai.teacher import generate_quiz, extract_topic
from ..utils.dependencies import get_current_user

router = APIRouter()


class QuizRequest(BaseModel):
    session_id: Optional[str] = None
    message: str


@router.post("/quiz")
def quiz(request: QuizRequest, user_id: int = Depends(get_current_user)):
    """Generate a quiz question for the given topic."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        topic = extract_topic(request.message)

        if request.session_id:
            # Verify session ownership
            cursor.execute(
                "SELECT id FROM sessions WHERE id=? AND user_id=?",
                (request.session_id, user_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=403, detail="Unauthorized session access")

            # Get mastery score for this topic
            cursor.execute("""
                SELECT t.mastery_score
                FROM topics t
                JOIN sessions s ON t.session_id = s.id
                WHERE t.session_id=? AND t.topic=? AND s.user_id=?
            """, (request.session_id, topic, user_id))

            row = cursor.fetchone()
            mastery_score = row[0] if row else 0.5
        else:
            mastery_score = 0.5

        quiz_content = generate_quiz(topic, mastery_score)

        return {
            "topic": topic,
            "mastery_score": mastery_score,
            "quiz": quiz_content
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation error: {str(e)}")
    finally:
        cursor.close()
        conn.close()