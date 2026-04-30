import pandas as pd
import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("data_preprocessing")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(os.path.join(LOG_DIR, "data_preprocessing.log"))
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = df.dropna()
        df["quiz_score"] = df["quiz_score"] / 100.0
        logger.debug("Data preprocessing completed")
        return df
    except Exception as e:
        logger.error("Preprocessing failed: %s", e)
        raise