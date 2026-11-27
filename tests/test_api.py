"""Integration checks for training, model selection and prediction logging."""
import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def api(tmp_path_factory):
    import os
    root = tmp_path_factory.mktemp("mlflow")
    os.environ["MLFLOW_TRACKING_URI"] = root.as_uri()
    import train
    import main
    importlib.reload(train)
    importlib.reload(main)
    train.train_models()
    with TestClient(main.app) as client:
        yield client


def test_models_predict_and_log(api):
    datasets = api.get("/api/datasets").json()
    models = api.get("/api/models").json()
    assert datasets[0]["id"] == "iris"
    assert len(models) == 2
    for model in models:
        response = api.post("/api/predict", json={"dataset_id": "iris", "model_id": model["id"], "features": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}})
        assert response.status_code == 200
        assert response.json()["species"] == "Setosa"
    runs = api.get("/api/runs").json()
    assert len([run for run in runs if run["tags"].get("kind") == "prediction"]) == 2
    assert all("accuracy" in model["metrics"] for model in models)


def test_rejects_invalid_inputs(api):
    model = api.get("/api/models").json()[0]
    payload = {"dataset_id": "iris", "model_id": model["id"], "features": {"sepal_length": -1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}}
    assert api.post("/api/predict", json=payload).status_code == 422
    payload["features"].pop("sepal_length")
    assert api.post("/api/predict", json=payload).status_code == 422
    payload["model_id"] = "unknown"
    assert api.post("/api/predict", json=payload).status_code == 404
