import logging
import os
import pandas as pd

from src.data_ingestion import load_params
from src.data_preprocessing import preprocess
from src.feature_engineering import create_features
from src.model_building import train_model

# ---------------- Logging ----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("training_pipeline")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(os.path.join(LOG_DIR, "training_pipeline.log"))
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def run_pipeline():
    try:
        logger.info("🚀 Training pipeline started")

        params = load_params("config/params.yaml")
        processed_path = params["data_ingestion"]["processed_data_path"]

        train_df = pd.read_csv(os.path.join(processed_path, "train.csv"))

        train_df = preprocess(train_df)
        X, y = create_features(train_df)

        train_model(X, y)

        logger.info("✅ Training pipeline completed successfully")

    except Exception as e:
        logger.critical("❌ Training pipeline failed: %s", e)
        raise


if __name__ == "__main__":
    run_pipeline()