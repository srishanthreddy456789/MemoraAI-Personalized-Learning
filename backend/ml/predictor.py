import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model", "model.pkl")

_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_weakness(features: dict) -> list:
    """
    Returns list of weak topics based on forgetting probability
    """
    model = load_model()

    X = [[
        features["last_studied_days"],
        features["revision_count"],
        features["quiz_score"]
    ]]

    prob = model.predict_proba(X)[0][1]

    if prob > 0.6:
        return ["concept_revision_needed"]
    return []