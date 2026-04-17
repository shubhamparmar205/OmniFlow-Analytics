import joblib
import pandas as pd
import os
from backend.schemas import TrafficPredictionRequest

# 1. Define where the model lives so we can load it into RAM once when the server starts
MODEL_PATH = os.path.join(os.getcwd(), 'ml_pipeline', 'saved_models', 'traffic_model.joblib')

# A global variable to keep the loaded model in memory
model = None

def load_system_model():
    """Loads the joblib model from the hard drive."""
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Backend Success: Machine Learning Model Loaded into RAM.")
    else:
        print("Backend Error: Could not find traffic_model.joblib. Did you run train_model.py?")

# 2. The core Logical Engine - Converts the API text into DataFrame math for the model
def run_prediction(request: TrafficPredictionRequest) -> dict:
    """Takes incoming JSON string data, transforms it into numbers, and calculates AI decision vectors."""
    
    # Safety Check
    global model
    if model is None:
        load_system_model()

    # A. Convert string timestamp to a datetime object
    dt = pd.to_datetime(request.timestamp)
    hour = dt.hour
    day_of_week = dt.dayofweek
    month = dt.month
    
    # B. Map the weather text
    weather_mapping = {'Clear': 0, 'Cloudy': 1, 'Rain': 2, 'Snow': 3}
    weather_encoded = weather_mapping.get(request.weather, 0)
    
    # C. Convert boolean True/False into 1 or 0
    events_encoded = 1 if request.events else 0
    
    # D. Package exact parameters
    input_df = pd.DataFrame([{
        'Hour': hour,
        'DayOfWeek': day_of_week,
        'Month': month,
        'Weather_Encoded': weather_encoded,
        'Events_Encoded': events_encoded
    }])
    
    # E. Final Full Output Prediction
    prediction_float = model.predict(input_df)[0]
    final_prediction = int(round(prediction_float))
    
    # F. LOGICAL INTERROGATION BLOCK (Option 1)
    # We forcefully run the AI multiple times stripping out factors to detect exactly WHY it chose its number
    
    # Base Traffic context (Assuming Weather=Clear, Events=None)
    baseline_df = pd.DataFrame([{'Hour': hour, 'DayOfWeek': day_of_week, 'Month': month, 'Weather_Encoded': 0, 'Events_Encoded': 0}])
    base_volume = int(round(model.predict(baseline_df)[0]))
    
    # Weather Impact (Assuming actual Weather, but Events=None)
    weather_df = pd.DataFrame([{'Hour': hour, 'DayOfWeek': day_of_week, 'Month': month, 'Weather_Encoded': weather_encoded, 'Events_Encoded': 0}])
    weather_volume = int(round(model.predict(weather_df)[0]))
    
    weather_impact = weather_volume - base_volume
    event_impact = final_prediction - weather_volume
    
    # G. Return a multi-dimensional dictionary payload
    return {
        "predicted_volume": final_prediction,
        "base_volume": base_volume,
        "weather_impact": weather_impact,
        "event_impact": event_impact
    }
