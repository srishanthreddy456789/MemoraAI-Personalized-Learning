import logging
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

# ---------------- Path Fix ----------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import load_params          # ✅ correct import
from src.data_preprocessing import preprocess
from src.feature_engineering import create_features
from src.model_building import train_model

# ---------------- Logging ----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("training_pipeline")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if not logger.handlers:
    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, "training_pipeline.log")
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# ---------------- Pipeline ----------------
def run_pipeline():
    try:
        logger.info("Training pipeline started")

        params = load_params("config/params.yaml")
        processed_path = params["data_ingestion"]["processed_data_path"]

        # Load processed data
        train_df = pd.read_csv(os.path.join(processed_path, "train.csv"))

        # Preprocess
        train_df = preprocess(train_df)

        # ✅ ADD THIS (REQUIRED TARGET COLUMN)
        train_df["forgotten"] = (train_df["quiz_score"] < 0.6).astype(int)

        # (optional debug – remove later)
        logger.debug("Columns before feature engineering: %s", train_df.columns.tolist())

        # Features & target
        X, y = create_features(train_df)

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=params["data_ingestion"]["test_size"],
            random_state=params["data_ingestion"]["random_state"],
        )

        # Train model (MLflow logging inside)
        train_model(X_train, y_train, X_test, y_test)

        logger.info("Training pipeline completed successfully")

    except Exception as e:
        logger.critical("Training pipeline failed: %s", e)
        raise


if __name__ == "__main__":
    run_pipeline()