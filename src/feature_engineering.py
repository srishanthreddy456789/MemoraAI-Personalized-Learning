import logging
import os
from src.utils import load_params

# ---------------- Logging ----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("feature_engineering")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if not logger.handlers:
    handler = logging.FileHandler(os.path.join(LOG_DIR, "feature_engineering.log"))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ---------------- Feature Engineering ----------------
def create_features(df):
    """
    Splits dataframe into features (X) and target (y)
    """
    try:
        params = load_params()

        feature_cols = params["features"]["input_features"]
        target_col = params["features"]["target"]

        X = df[feature_cols]
        y = df[target_col]

        logger.info(
            "Created features with %d rows and %d columns",
            X.shape[0],
            X.shape[1]
        )

        return X, y

    except KeyError as e:
        logger.error("Missing required column: %s", e)
        raise

    except Exception as e:
        logger.error("Feature engineering failed: %s", e)
        raise