from pydantic import BaseModel
from typing import Optional

class PredictionRequest(BaseModel):
    pm25: float
    pm10: float
    so2: float
    no2: float
    co: float
    o3: float
    temperature: float
    humidity: float
    wind_speed: float
    pressure: float

class PredictionResponse(BaseModel):
    aqi: float
    level: str
    color: str
    pm25: float
    pm10: float
    so2: float
    no2: float
    co: float
    o3: float
