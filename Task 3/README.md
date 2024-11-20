# Iris Classification API with Docker

## Overview
This project implements a machine learning logistic regression model to classify Iris flowers using FastAPI, enhanced with Docker containerization.

## Features
- REST API endpoint for Iris species prediction
- Web interface for model interaction
- Docker containerization
- Trained machine learning model using Iris dataset
- FastAPI for efficient API handling
- Joblib for model serialization

## Prerequisites
- Docker
- Git

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

## Installation & Setup

### 1. Clone Repository with Sparse Checkout
```bash
git clone --no-checkout https://github.com/ibrahimsabouh/Qafza-Tasks.git
cd Qafza-Tasks
git sparse-checkout init
git sparse-checkout set "Task 3"
git checkout main
cd "Task 3"
```

### 2. Build Docker Image
```bash
docker build -t iris-classification-api .
```

### 3. Run Docker Container
```bash
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

## Dockerfile Explanation
The Dockerfile performs these key steps:
- Uses Python 3.9 slim base image
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

## Docker Rebuild
If you modify the code or dependencies:
```bash
docker build -t iris-classification-api .
docker run -p 8000:8000 iris-classification-api
```

## Contact
Ibrahim Sabouh
- Email: ibrahim.sabouh7@gmail.com
- GitHub: [ibrahimsabouh](https://github.com/ibrahimsabouh/Qafza-Tasks)

## License
[Specify your license here]
