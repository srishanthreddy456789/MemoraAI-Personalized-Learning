import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from src.utils import load_params
import os

def train_model(X_train, y_train, X_test, y_test):
    params = load_params()

    model_params = params["model"]
    experiment_name = params["mlflow"]["experiment_name"]

    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        model = LogisticRegression(
            max_iter=model_params["max_iter"],
            random_state=model_params["random_state"]
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_metric("accuracy", acc)

        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="forgetting_model"
        )

        os.makedirs("models", exist_ok=True)
        mlflow.sklearn.save_model(model, "models/model")

        return acc