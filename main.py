"""Iris prediction API backed by MLflow's file-based tracking store."""
import math
import os
from pathlib import Path
from typing import Annotated

import mlflow
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from mlflow.tracking import MlflowClient
from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parent
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", (ROOT / "mlruns").as_uri()))
app = FastAPI(title="Iris ML Studio")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:4200"], allow_methods=["*"], allow_headers=["*"])
FEATURES = [
    {"id": "sepal_length", "label": "Sepal length", "column": "sepal length (cm)", "unit": "cm"},
    {"id": "sepal_width", "label": "Sepal width", "column": "sepal width (cm)", "unit": "cm"},
    {"id": "petal_length", "label": "Petal length", "column": "petal length (cm)", "unit": "cm"},
    {"id": "petal_width", "label": "Petal width", "column": "petal width (cm)", "unit": "cm"},
]
DATASET = {"id": "iris", "name": "Iris flowers", "description": "Classify iris species from four flower measurements.", "features": FEATURES}


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    dataset_id: str
    model_id: str
    features: dict[str, Annotated[float, Field(strict=True)]]


def runs(experiment_name):
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if not experiment:
        return []
    return client.search_runs([experiment.experiment_id], order_by=["attributes.start_time DESC"])


def model_catalog():
    latest = {}
    for run in runs("iris-training"):
        name = run.data.tags.get("model_name")
        if run.info.status == "FINISHED" and run.data.tags.get("dataset") == "iris" and name and name not in latest:
            latest[name] = {"id": run.info.run_id, "name": name, "dataset_id": "iris", "metrics": run.data.metrics, "params": run.data.params}
    return list(latest.values())


@app.get("/api/datasets")
def datasets():
    return [DATASET]


@app.get("/api/models")
def models():
    return model_catalog()


@app.get("/api/runs")
def list_runs():
    return [{"id": run.info.run_id, "name": run.data.tags.get("mlflow.runName", "Run"), "status": run.info.status,
             "started_at": run.info.start_time, "metrics": run.data.metrics, "params": run.data.params,
             "tags": run.data.tags} for experiment in ("iris-training", "iris-predictions") for run in runs(experiment)]


@app.post("/api/predict")
def predict(request: PredictionRequest):
    if request.dataset_id != "iris":
        raise HTTPException(404, "Unknown dataset")
    if request.model_id not in {model["id"] for model in model_catalog()}:
        raise HTTPException(404, "Model is not available for this dataset")
    if set(request.features) != {feature["id"] for feature in FEATURES} or any(not math.isfinite(value) or value <= 0 for value in request.features.values()):
        raise HTTPException(422, "Provide a positive finite number for each feature")
    frame = pd.DataFrame([[request.features[feature["id"]] for feature in FEATURES]], columns=[feature["column"] for feature in FEATURES])
    model = mlflow.sklearn.load_model(f"runs:/{request.model_id}/model")
    result = int(model.predict(frame)[0])
    species = ["Setosa", "Versicolor", "Virginica"][result]
    client = MlflowClient()
    experiment = client.get_experiment_by_name("iris-predictions")
    experiment_id = experiment.experiment_id if experiment else client.create_experiment("iris-predictions")
    run = client.create_run(experiment_id, tags={"mlflow.runName": "Prediction", "kind": "prediction", "model_run_id": request.model_id, "dataset": request.dataset_id})
    try:
        for key, value in request.features.items():
            client.log_param(run.info.run_id, key, value)
        client.log_param(run.info.run_id, "prediction", species)
        client.set_terminated(run.info.run_id, "FINISHED")
    except Exception:
        client.set_terminated(run.info.run_id, "FAILED")
        raise
    return {"species": species, "model_id": request.model_id}


browser = ROOT / "static"
if browser.exists():
    app.mount("/assets", StaticFiles(directory=browser / "assets"), name="assets") if (browser / "assets").exists() else None
    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str):
        candidate = (browser / path).resolve()
        if candidate.is_file() and browser.resolve() in candidate.parents:
            return FileResponse(candidate)
        return FileResponse(browser / "index.html")

