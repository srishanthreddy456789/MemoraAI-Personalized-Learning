import pandas as pd
import os
import logging
from sklearn.model_selection import train_test_split
from src.utils import load_params

# ---------------- Logging ----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("data_ingestion")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if not logger.handlers:
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "data_ingestion.log"))
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# ---------------- Core Logic ----------------
def load_data() -> pd.DataFrame:
    params = load_params("config/params.yaml")
    path = params["data_ingestion"]["raw_data_path"]

    df = pd.read_csv(path)
    logger.info("Loaded raw data from %s", path)
    return df


def split_and_save(df: pd.DataFrame):
    params = load_params("config/params.yaml")

    cfg = params["data_ingestion"]
    test_size = cfg["test_size"]
    random_state = cfg["random_state"]
    out_dir = cfg["processed_data_path"]

    os.makedirs(out_dir, exist_ok=True)

    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state
    )

    train_df.to_csv(os.path.join(out_dir, "train.csv"), index=False)
    test_df.to_csv(os.path.join(out_dir, "test.csv"), index=False)

    logger.info("Saved train.csv and test.csv to %s", out_dir)


def main():
    logger.info("Starting data ingestion")
    df = load_data()
    split_and_save(df)
    logger.info("Data ingestion completed successfully")


if __name__ == "__main__":
    main()