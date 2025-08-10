from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from typing import List
import logging
from app.services import AirQualityPredictor
from app.schemas import PredictionRequest, PredictionResponse
from fastapi import Request

# Initialize FastAPI app
app = FastAPI(
    title="Air Quality Prediction API",
    description="API for predicting air quality using LSTM model",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
predictor = AirQualityPredictor()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Air Quality Prediction API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": predictor.model is not None}

@app.post("/predict", response_model=PredictionResponse)
async def predict_air_quality(request: PredictionRequest, fastapi_request: Request):
    """Predict air quality based on input features"""
    try:
        logger.info(f"Received prediction request: {request}")
        
        # Prepare input data
        features = [
            request.pm25,
            request.pm10,
            request.so2,
            request.no2,
            request.co,
            request.o3,
            request.temperature,
            request.humidity,
            request.wind_speed,
            request.pressure
        ]
        
        # Make prediction
        prediction = predictor.predict(features)
        
        # Determine air quality level
        aqi = prediction['aqi']
        if aqi <= 50:
            level = "Good"
            color = "#00e400"
        elif aqi <= 100:
            level = "Moderate"
            color = "#ffff00"
        elif aqi <= 150:
            level = "Unhealthy for Sensitive Groups"
            color = "#ff7e00"
        elif aqi <= 200:
            level = "Unhealthy"
            color = "#ff0000"
        elif aqi <= 300:
            level = "Very Unhealthy"
            color = "#8f3f97"
        else:
            level = "Hazardous"
            color = "#7e0023"
        
        return PredictionResponse(
            aqi=aqi,
            level=level,
            color=color,
            pm25=request.pm25,
            pm10=request.pm10,
            so2=request.so2,
            no2=request.no2,
            co=request.co,
            o3=request.o3
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    return {
        "model_type": "LSTM",
        "features": ["pm25", "pm10", "so2", "no2", "co", "o3", "temperature", "humidity", "wind_speed", "pressure"],
        "output": "AQI (Air Quality Index)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
