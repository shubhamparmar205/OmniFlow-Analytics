from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as prediction_router
from backend.services.prediction import load_system_model

# 1. Create the overarching server Application object
app = FastAPI(
    title="Smart-City Traffic AI API",
    description="The fast prediction engine connecting the UI to the XGBoost model.",
    version="1.0.0"
)

# 2. CORS configuration is MANDATORY! Without this, a Chrome web browser completely blocks our local HTML files from getting API data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For this test project, we allow any HTML website to connect to our server
    allow_credentials=True,
    allow_methods=["*"], # Allow everything (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],
)

# 3. Before the server allows users to connect, physically load the heavy Machine Learning Model into your machine's RAM
@app.on_event("startup")
async def startup_event():
    load_system_model()

# 4. Attach the specific routes (URLs) from our API folder into the main application
app.include_router(prediction_router)

from pathlib import Path
from fastapi.staticfiles import StaticFiles

# 5. Dynamically resolve the absolute path to prevent Render/Linux deployment crashes
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Serve the User Interface directly!
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
