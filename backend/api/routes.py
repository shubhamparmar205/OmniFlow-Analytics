from fastapi import APIRouter, HTTPException
from backend.schemas import TrafficPredictionRequest, TrafficPredictionResponse
from backend.services.prediction import run_prediction, model

# 1. Create a "Router" which acts as a sub-menu to organize our API endpoints cleanly
router = APIRouter()

# 2. Open up the POST endpoint where the website will continuously send JSON data
@router.post("/predict", response_model=TrafficPredictionResponse)
def get_prediction(request: TrafficPredictionRequest):
    """Receives JSON from frontend, passes it to the ML engine, and returns the finished result."""

        
    try:
        # Run the complex AI interrogation logic inside our services script
        response_dict = run_prediction(request)
        
        # Package and return the multi-layered analysis payload back to the internet
        return TrafficPredictionResponse(**response_dict)
        
    except Exception as e:
        # If something crashes (e.g. wrong datetime text structure sent), gracefully tell the user
        raise HTTPException(status_code=400, detail=f"Failed to process prediction: {str(e)}")
