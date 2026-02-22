from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import logging

# ---------------- Logging ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi")

# ---------------- App ----------------
app = FastAPI(
    title="MemoraAI API",
    description="Forgetting Prediction using MLflow + FastAPI",
    version="1.0"
)

# ---------------- Load Config ----------------
def load_params(path="config/params.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

params = load_params()

# ---------------- Load Model from MLflow ----------------
mlflow.set_experiment(params["mlflow"]["experiment_name"])

MODEL_URI = "models:/forgetting_model/Production"

try:
    model = mlflow.sklearn.load_model(MODEL_URI)
    logger.info("✅ Model loaded from MLflow Registry")
except Exception as e:
    logger.error("❌ Failed to load model: %s", e)
    model = None

# ---------------- Request Schema ----------------
class PredictionRequest(BaseModel):
    last_studied_days: int
    quiz_score: float
    revision_count: int

# ---------------- Health Check ----------------
@app.get("/")
def health_check():
    return {"status": "FastAPI is running 🚀"}

# ---------------- Prediction Endpoint ----------------
@app.post("/predict")
def predict_forgetting(data: PredictionRequest):
    if model is None:
        return {"error": "Model not loaded"}

    input_df = pd.DataFrame([data.dict()])
    probability = model.predict_proba(input_df)[0][1]

    return {
        "forgetting_probability": round(float(probability), 3),
        "risk_level": "HIGH" if probability > 0.6 else "LOW"
    }