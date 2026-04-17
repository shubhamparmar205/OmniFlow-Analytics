from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal

# 1. This class defines the exact shape of the data we expect from the frontend
class TrafficPredictionRequest(BaseModel):
    timestamp: str  
    # Concept 9 (Security & Validation): Force weather to match EXACTLY one of these strings.
    weather: Literal["Clear", "Cloudy", "Rain", "Snow"]
    events: bool    

# 2. This class defines the exact shape of the response we send back to the frontend
class TrafficPredictionResponse(BaseModel):
    predicted_volume: int
    base_volume: int
    weather_impact: int
    event_impact: int
    
    # Simple setting to allow Pydantic to read standard dictionaries if needed
    model_config = ConfigDict(from_attributes=True)
