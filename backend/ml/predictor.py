import joblib
import os

# ✅ FIXED: Graceful fallback when ML model file is not present on Render
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model", "model.pkl")

_model = None


def load_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            _model = None  # Model not available in this environment
    return _model


def predict_weakness(features: dict) -> list:
    """
    Returns list of weak topic flags based on ML model prediction.
    Falls back to a rule-based heuristic if model is not available.
    """
    model = load_model()

    if model is not None:
        try:
            import numpy as np
            X = [[
                features.get("last_studied_days", 0),
                features.get("revision_count", 0),
                features.get("quiz_score", 0.5)
            ]]
            return model.predict(X).tolist()
        except Exception:
            pass

    # Rule-based fallback: topic is "weak" if quiz score < 0.5 or not studied recently
    quiz_score = features.get("quiz_score", 0.5)
    days = features.get("last_studied_days", 999)
    is_weak = (quiz_score < 0.5) or (days > 7)
    return [1 if is_weak else 0]