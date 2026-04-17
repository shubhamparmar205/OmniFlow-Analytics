import pytest
from fastapi.testclient import TestClient
from backend.main import app

# Create a test client that mocks a web browser talking to our app
client = TestClient(app)

def test_api_health_check():
    """Validates the server serves the Frontend GUI properly."""
    response = client.get("/")
    assert response.status_code == 200
    # It now serves HTML directly! Test for successful HTML detection.
    assert "text/html" in response.headers["content-type"]
    assert "Mission Control" in response.text

def test_prediction_success():
    """Validates that correct data returns a valid integer prediction."""
    payload = {
        "timestamp": "2023-11-25T14:30:00",
        "weather": "Rain",
        "events": True
    }
    response = client.post("/predict", json=payload)
    
    # Assert Http Status was 200 OK
    assert response.status_code == 200
    
    # Assert the returned JSON contains our predicted_volume
    data = response.json()
    assert "predicted_volume" in data
    
    # Ensure what we returned was a pure integer
    assert isinstance(data["predicted_volume"], int)

def test_prediction_security_validation():
    """Validates Concept 9: Bad data (like a wrong Weather String) is securely blocked."""
    payload = {
        "timestamp": "2023-11-25T14:30:00",
        "weather": "HACKER_ATTACK_STRING", # The Strict Literal we just added MUST catch this
        "events": True
    }
    response = client.post("/predict", json=payload)
    
    # Assert Http Status is 422 Unprocessable Entity (FastAPI automatically caught and blocked it!)
    assert response.status_code == 422
