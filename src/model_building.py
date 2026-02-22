import mlflow
import mlflow.sklearn
import yaml
import logging
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger("model_building")
logger.setLevel(logging.DEBUG)

def load_params(path="config/params.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def train_model(X, y):
    try:
        params = load_params()

        mlflow.set_experiment(params["mlflow"]["experiment_name"])

        with mlflow.start_run():
            model = LogisticRegression(
                max_iter=params["model"]["max_iter"],
                random_state=params["model"]["random_state"]
            )

            model.fit(X, y)
            acc = model.score(X, y)

            mlflow.log_metric("accuracy", acc)
            mlflow.sklearn.log_model(model, "forgetting_model")

            logger.debug("Model trained and logged to MLflow")

        return model
    except Exception as e:
        logger.error("Model training failed: %s", e)
        raise