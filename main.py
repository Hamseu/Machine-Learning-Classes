from fastapi import FastAPI
from starlette.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import pandas as pd

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float







app = FastAPI()

model = joblib.load("model.joblib")

@app.get("/")
def home():
    return {"message": " API is running"}


@app.post("/predict")
def predict(data: IrisInput):

    features = pd.DataFrame(
        [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]],
        columns=[
            "sepal length (cm)",
            "sepal width (cm)",
            "petal length (cm)",
            "petal width (cm)"
        ]
    )

    prediction = model.predict(features)[0]

    species = ["Setosa", "Versicolor", "Virginica"]

    return {
        "prediction": int(prediction),
        "species": species[int(prediction)]
    }

