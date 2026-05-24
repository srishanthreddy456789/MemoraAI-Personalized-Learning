from fastapi import APIRouter
from pydantic import BaseModel
from ..ml.predictor import predict_weakness

router = APIRouter()


class PredictRequest(BaseModel):
    last_studied_days: int
    revision_count: int
    quiz_score: float


@router.post("/predict")
def predict(request: PredictRequest):
    """Predict whether a topic is a weakness based on study features."""
    features = {
        "last_studied_days": request.last_studied_days,
        "revision_count": request.revision_count,
        "quiz_score": request.quiz_score,
    }
    result = predict_weakness(features)
    return {
        "prediction": result,
        "is_weak": bool(result[0] == 1)
    }