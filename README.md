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
Clone the repository:

```bash
git clone https://github.com/Hamseu/Machine-Learning-Classes.git
cd Machine-Learning-Classes
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Model Training

Train and save the machine learning model:

```bash
python train.py
```

The trained model is saved as `model.joblib`.

## Running the API Locally

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

- Root endpoint: http://localhost:8000/
- Swagger documentation: http://localhost:8000/docs

## API Endpoints

### GET /

Checks whether the API is running.

Example response:

```json
{
    "message": "API is running"
}
```

### POST /predict

Accepts four numerical features and returns the predicted Iris species.

Example request:

```json
{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
```

Example response:

```json
{
    "prediction": 0,
    "species": "Setosa"
}
```

### Target Classes

| Class | Species |
|-------|------------|
| 0     | Setosa     |
| 1     | Versicolor |
| 2     | Virginica  |

## Running with Docker

*Docker must be installed and running before executing commands below*

### Build the Docker Image

```bash
docker build -t iris-api .
```

### Run the Docker Container

```bash
docker run -d -p 8000:8000 --name simple-ml-api iris-api
```

### Verify the Running Container

```bash
docker ps
```
### Stop the Container

```bash
docker stop simple-ml-api
```

### Restart the Container

```bash
docker start simple-ml-api
```

## API Testing

1. Open http://localhost:8000/docs.
2. Select the POST /predict endpoint.
3. Click "Try it out".
4. Enter the input features in JSON format.
5. Click "Execute".
6. Verify the prediction and HTTP status code.

   Both docker version and local are working well.
