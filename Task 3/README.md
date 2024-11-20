# Iris Classification API with Docker

## Overview
This project implements a machine learning logistic regression model to classify Iris flowers using FastAPI, containerized with Docker for easy deployment.

## Features
- REST API endpoint for Iris species prediction
- Web interface for model interaction
- Docker containerization
- Trained machine learning model using Iris dataset
- FastAPI for efficient API handling
- Joblib for model serialization

## Project Structure
```
.
├── Dockerfile           # Docker configuration
├── app.py               # FastAPI application and API endpoints
├── model.py             # Model training script
├── model.joblib         # Saved trained model
├── requirements.txt     # Python dependencies
├── templates/         
│   └── index.html       # Web interface template
└── README.md            # Project documentation
```

## Running the Application

### Option 1: Using DockerHub Image (required Docker installed)
1. Pull and Run the Docker image:
```bash
docker pull ibrahimsabouh/iris-classification-api
docker run -p 8000:8000 ibrahimsabouh/iris-classification-api
```

### Option 2: Local Build
1. Clone the repository and navigate to the folder
```bash
git clone --no-checkout https://github.com/ibrahimsabouh/Qafza-Tasks.git
cd Qafza-Tasks
```

2. Set up sparse checkout and download only the Task 3 folder
```bash
git sparse-checkout init
git sparse-checkout set "Task 3"
git checkout main
cd "Task 3"
```

3. Build and Run the Docker image:
```bash
docker build -t iris-classification-api .
docker run -p 8000:8000 iris-classification-api
```

## Accessing the Application
- Web Interface: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

### Making Predictions
1. Web Interface:
   - Visit `http://localhost:8000`
   - Enter Iris measurements
   - Click "Predict"

2. API Endpoint:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## Requirements

### Software
- Python 3.9+
- Docker
- Git (for cloning the repository)

### Python Dependencies
The project requires the following Python packages:
- fastapi
- uvicorn
- scikit-learn
- joblib
- pydantic
- jinja2

You can install these dependencies using the requirements.txt file:
```bash
pip install -r requirements.txt
```

## Dockerfile Explanation
The Dockerfile performs these key steps:
- Uses Python 3.9 slim base imag
- Sets working directory
- Copies project files
- Installs dependencies
- Exposes port 8000
- Launches FastAPI application using Uvicorn

## Development
To retrain the model locally:
```bash
python model.py
```

## Contact
Ibrahim Sabouh
- Email: ibrahim.sabouh7@gmail.com
- GitHub: [ibrahimsabouh](https://github.com/ibrahimsabouh/Qafza-Tasks)
