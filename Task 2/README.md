# Iris Classification API

A FastAPI-based web application that predicts Iris flower species using a machine learning model trained on the famous Iris dataset.

## Overview

This project implements a machine learning logistic regression model to classify Iris flowers based on their measurements. It provides both a REST API endpoint and a web interface for making predictions.

## Features

- REST API endpoint for Iris species prediction
- Web interface for easy interaction with the model
- Trained machine learning model using the Iris dataset
- FastAPI for efficient API handling
- Joblib for model serialization

## Project Structure

```
.
├── app.py              # FastAPI application and API endpoints
├── model.py            # Model training script
├── model.joblib        # Saved trained model
├── templates/         
│   └── index.html      # Web interface template
└── README.md           # Project documentation
```

## Installation

1. Clone the repository and navigate to Task 2:
```bash
git clone https://github.com/ibrahimsabouh/Qafza-Tasks.git
cd "Qafza-Tasks/Task 2"
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install numpy fastapi uvicorn scikit-learn joblib pydantic
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn app:app --reload
# or
python app.py
```

2. Access the application:
   - Web Interface: Open `http://localhost:8000` in your web browser
   - API Documentation: Visit `http://localhost:8000/docs`

### Making Predictions

You can make predictions in two ways:

1. Through the web interface:
   - Visit `http://localhost:8000`
   - Enter the Iris measurements
   - Click "Predict"

2. Using the API directly:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## Model Details

The model is trained on the Iris dataset using scikit-learn. The dataset contains measurements for three Iris species:
- Setosa
- Versicolor
- Virginica

Features used for prediction:
- Sepal Length (cm)
- Sepal Width (cm)
- Petal Length (cm)
- Petal Width (cm)

## Development

To retrain the model:
```bash
python model.py
```

## Contact

Ibrahim Sabouh
- Email: ibrahim.sabouh7@gmail.com
- GitHub: [ibrahimsabouh](https://github.com/ibrahimsabouh/Qafza-Tasks)