# Iris ML Studio

A full-cycle Iris classification application with FastAPI, Angular, Tailwind CSS and MLflow. Train logistic regression and random forest models, predict flower species, and inspect training metrics and prediction logs. MLflow stores runs and model artifacts in files; no database or login is required.

## Docker

```sh
docker build -t iris-studio .
docker run --rm -p 8000:8000 -v iris-mlruns:/app/mlruns -v iris-evaluation:/app/evaluation iris-studio
```

Open http://localhost:8000. On a fresh tracking volume the container trains the models at startup. Runs and evaluation reports persist in the named volumes. To retrain, run `docker exec <container> python train.py`; the latest successful run of each model is offered for prediction. Do not share a file store between multiple independent writers.

## Local development

Use Python 3.12 and Node.js 20.19+ (or 22.12+). From the project root:

```sh
python -m venv .venv
# Activate the virtual environment, then:
pip install -r requirements.txt
python train.py
uvicorn main:app --reload
```

In another terminal:

```sh
cd ml-system-app
npm install
npm start
```

Open http://localhost:4200. API documentation is at http://localhost:8000/docs. To inspect MLflow's native UI, run `python start_mlflow.py` from the project root and open http://localhost:5000. The application also includes an Experiments page showing run parameters, metrics, and prediction logs. MLflow artifacts are under `mlruns/`; evaluation reports are under `evaluation/`. Set `MLFLOW_TRACKING_URI` to the same file URI for training, the API, and the UI to choose another store. The local MLflow UI reads the local store; runs inside Docker remain in the Docker volume and are separate.

## Tests

```sh
python -m pytest tests
cd ml-system-app
npm run build
```

The API accepts positive finite measurements in centimetres, validates feature names and model/dataset compatibility, and returns a species name. The example Iris measurements 5.1, 3.5, 1.4, 0.2 predict Setosa.

