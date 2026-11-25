# Machine-Learning-Classes

Currently this is practice work 6 made by Frolov Yevgeniy

## Description:
This is prototype of ML system, it was trained on IRIS dataset using logistical regression. It's built on fast-api. Its container is virtualized using docker.

## Items:
Dockerfile - settings for docker
Main.py - main file of fast-api
model.joblib - artifact of our model
Requirements.txt - list of dependencies and their versions
train.py - file with training of model

## Instructions:
4. Installation

Clone the repository:

git clone YOUR_REPOSITORY_URL
cd ml-fastapi-docker

Install the required dependencies:

pip install -r requirements.txt

5. Model Training

To train the model and generate the model.joblib file, execute:

python train.py

This step can be skipped if the trained model file already exists.

6. Running the API Locally

Start the FastAPI application using Uvicorn:

python -m uvicorn main:app --reload

The API will be available at:

Root endpoint: http://localhost:8000/

Swagger documentation: http://localhost:8000/docs

7. API Endpoints

GET /

Checks whether the API is running.

Example response:

{
    "message": "ML API is running"
}

POST /predict

Accepts four numerical features and returns a predicted Iris species.

Example request:

{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

Example response:

{
    "prediction": 0,
    "species": "Setosa"
}

Target classes:

Class

Species

0

Setosa

1

Versicolor

2

Virginica

8. Running with Docker

Docker must be installed and running before executing the following commands.

Build the Docker image

docker build -t iris-api .

Run the Docker container

docker run -d -p 8000:8000 --name iris-container iris-api

Verify that the container is running

docker ps

View application logs

docker logs iris-container

Stop the container

docker stop iris-container

Restart the container

docker start iris-container
