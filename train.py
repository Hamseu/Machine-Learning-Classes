"""Train Iris classifiers and record their artifacts and evaluations in MLflow."""
import json
import os
from pathlib import Path

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", (ROOT / "mlruns").as_uri())


def train_models():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment("iris-training")
    iris = load_iris(as_frame=True)
    train_x, test_x, train_y, test_y = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    models = {
        "Logistic regression": LogisticRegression(max_iter=500, random_state=42),
        "Random forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }
    (ROOT / "evaluation").mkdir(exist_ok=True)
    (ROOT / "models").mkdir(exist_ok=True)
    for name, model in models.items():
        with mlflow.start_run(run_name=name) as run:
            model.fit(train_x, train_y)
            predictions = model.predict(test_x)
            report = classification_report(test_y, predictions, target_names=iris.target_names, output_dict=True)
            mlflow.set_tags({"dataset": "iris", "model_name": name, "kind": "training"})
            mlflow.log_params(model.get_params())
            mlflow.log_metrics({"accuracy": accuracy_score(test_y, predictions), "f1_macro": f1_score(test_y, predictions, average="macro")})
            mlflow.log_dict(report, "evaluation/classification_report.json")
            mlflow.sklearn.log_model(model, "model", input_example=train_x.head(1))
            (ROOT / "evaluation" / f"{run.info.run_id}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(f"{name}: {run.info.run_id}")


if __name__ == "__main__":
    train_models()
