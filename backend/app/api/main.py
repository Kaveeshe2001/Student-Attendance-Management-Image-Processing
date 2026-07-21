from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database.database import engine, Base
from app.api.routers import process, results, statistics, logs, visualizations, sessions

# Initialize SQLite tables on startup
Base.metadata.create_all(bind=engine)

# Ensure results directory exists for static mounting
os.makedirs("./results", exist_ok=True)

app = FastAPI(
    title="SAMS REST API Backend",
    description="REST API for the AI-powered Student Attendance Management System (SAMS)",
    version="1.0"
)

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder results/ to render visualization images locally
app.mount("/results", StaticFiles(directory="results"), name="results")

# Register Routers
app.include_router(process.router)
app.include_router(results.router)
app.include_router(statistics.router)
app.include_router(logs.router)
app.include_router(visualizations.router)
app.include_router(sessions.router)

@app.get("/")
def read_root():
    return {
        "title": "SAMS Backend API",
        "status": "online",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
