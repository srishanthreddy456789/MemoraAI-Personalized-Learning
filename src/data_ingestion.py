import pandas as pd
import os
import yaml
import logging
from sklearn.model_selection import train_test_split

# ---------------- Logging ----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("data_ingestion")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "data_ingestion.log"))
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ---------------- Utils ----------------
def load_params(path: str) -> dict:
    try:
        with open(path, "r") as f:
            params = yaml.safe_load(f)
        logger.debug("Loaded params from %s", path)
        return params
    except Exception as e:
        logger.error("Failed to load params: %s", e)
        raise

def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        logger.debug("Loaded data from %s", path)
        return df
    except Exception as e:
        logger.error("Failed to load data: %s", e)
        raise

def split_and_save(df: pd.DataFrame, params: dict):
    try:
        test_size = params["data_ingestion"]["test_size"]
        random_state = params["data_ingestion"]["random_state"]
        out_dir = params["data_ingestion"]["processed_data_path"]

        os.makedirs(out_dir, exist_ok=True)

        train_df, test_df = train_test_split(
            df, test_size=test_size, random_state=random_state
        )

        train_df.to_csv(os.path.join(out_dir, "train.csv"), index=False)
        test_df.to_csv(os.path.join(out_dir, "test.csv"), index=False)

        logger.debug("Train/Test data saved to %s", out_dir)
    except Exception as e:
        logger.error("Failed during train-test split: %s", e)
        raise

def main():
    try:
        params = load_params("config/params.yaml")
        raw_path = params["data_ingestion"]["raw_data_path"]

        df = load_data(raw_path)
        split_and_save(df, params)

        logger.info("✅ Data ingestion completed successfully")

    except Exception as e:
        logger.critical("❌ Data ingestion failed: %s", e)
        raise

if __name__ == "__main__":
    main()