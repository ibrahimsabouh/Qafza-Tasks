from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="joblib")

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

try:
    model = joblib.load("model.joblib")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading model: {e}")

# Iris species labels
iris_species = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}

# Define the structure of the input data for the API
class ModelInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float

# Home page with HTML form
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Prediction API endpoint
@app.post("/predict")
def predict_api(input: ModelInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    features = np.array([[input.feature1, input.feature2, input.feature3, input.feature4]])
    prediction = model.predict(features)
    species = iris_species.get(prediction[0], "Unknown")
    
    return {"prediction": species}

# Form submission endpoint
@app.post("/predict_form", response_class=HTMLResponse)
def predict_form(
    request: Request,
    feature1: float = Form(...),
    feature2: float = Form(...),
    feature3: float = Form(...),
    feature4: float = Form(...)
):
    if model is None:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Model not loaded"})

    features = np.array([[feature1, feature2, feature3, feature4]])
    prediction = model.predict(features)
    species = iris_species.get(prediction[0], "Unknown")
    
    return templates.TemplateResponse("index.html", {"request": request, "prediction": species})

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)