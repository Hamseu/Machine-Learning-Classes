# Iris-Api

GitHub Link - https://github.com/Hamseu/Machine-Learning-Classes.git  
To see new version with front - check front-version branch of repo.
A full-cycle Iris classification application with FastAPI, Angular, Tailwind CSS and MLflow. I have trained Train logistic regression and random forest models to predict flower species, and inspect training metrics and prediction logs. MLflow stores runs, model artifacts in files.

## Docker

```sh
docker build -t iris-api .
docker run -d -p 8000:8000 --name ml-model iris-api
```

Open http://localhost:8000. On a fresh tracking volume the container trains the models at startup. Runs and evaluation reports persist in the named volumes. To retrain, run `docker exec <container> python train.py`; the latest successful run of each model is offered for prediction.

## Local development

Use Python 3.12 and Node.js 20.19+ (or 22.12+). From the project root:

```sh
pip install -r requirements.txt
python train.py
uvicorn main:app --reload
```

In another terminal(This one is for angular):

```sh
cd ml-system-app
npm install
npm start
``` 

Open http://localhost:4200. API documentation is at http://localhost:8000/docs. To inspect MLflow's native UI, run `python start_mlflow.py` from the project root and open http://localhost:5000. The application also includes an Experiments page showing run parameters, metrics, and prediction logs. MLflow artifacts are under `mlruns/`, not `mlruns/`/``; evaluation reports are under `evaluation/`. The local MLflow UI reads the local store; runs inside Docker remain in the Docker volume and are separate.

## Tests, There are some, but they mostly were needed for deploying

```sh
python -m pytest tests
cd ml-system-app
npm run build
```

The API accepts positive finite measurements in centimetres, validates feature names and model/dataset compatibility, and returns a species name.

