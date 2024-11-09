from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Load Titanic model
try:
    model = joblib.load('Titanic_Model.joblib')
except Exception as e:
    raise Exception(f"Error loading the model: {str(e)}")

# Define the input data model with proper types
class TitanicInput(BaseModel):
    Pclass: int
    Sex: int
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked_Q: bool
    Embarked_S: bool

@app.get('/')
def index():
    return {'message': 'Titanic Model'}

@app.post("/predict")
async def predict(data: TitanicInput):
    try:
        # Convert input features to numpy array in the correct order
        features = np.array([
            data.Pclass,
            data.Sex,
            data.Age,
            data.SibSp,
            data.Parch,
            data.Fare,
            data.Embarked_Q,
            data.Embarked_S
        ]).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        
        return {
            "prediction": int(prediction),
            "probability": float(probability)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)