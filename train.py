import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib



df = load_iris(as_frame=True).frame

X = df.drop(columns = ["target"])
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)
model = LogisticRegression()

model.fit(X_train, y_train)
joblib.dump(model, "model.joblib")

loaded_model = joblib.load("model.joblib")

if loaded_model.predict(X_test) is None:
    print("Model load failed")