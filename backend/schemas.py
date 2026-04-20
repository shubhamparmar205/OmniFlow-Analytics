from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Literal

# 1. This class defines the exact shape of the data we expect from the frontend
class TrafficPredictionRequest(BaseModel):
    timestamp: str  
    weather: Literal["Clear", "Cloudy", "Rain", "Snow"]
    events: bool    

    # Security Feature: Reject inference data from the past to protect the prediction framework integrity
    @field_validator('timestamp')
    @classmethod
    def check_future_timestamp(cls, v: str):
        input_dt = datetime.fromisoformat(v)
        # Compare submitted timestamp directly against active local server machine time
        if input_dt < datetime.now():
            raise ValueError("Timestamp cannot be historically dated. This is an explicit Future Prediction Framework.")
        return v

# 2. This class defines the exact shape of the response we send back to the frontend
class TrafficPredictionResponse(BaseModel):
    predicted_volume: int
    base_volume: int
    weather_impact: int
    event_impact: int
    
    # Simple setting to allow Pydantic to read standard dictionaries if needed
    model_config = ConfigDict(from_attributes=True)
