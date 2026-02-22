import yaml
import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("feature_engineering")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(os.path.join(LOG_DIR, "feature_engineering.log"))
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

def load_params(path="config/params.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def create_features(df):
    try:
        params = load_params()
        features = params["features"]["input_features"]
        threshold = params["features"]["quiz_score_threshold"]

        X = df[features]
        y = (df["quiz_score"] < threshold).astype(int)

        logger.debug("Feature engineering completed")
        return X, y
    except Exception as e:
        logger.error("Feature engineering failed: %s", e)
        raise