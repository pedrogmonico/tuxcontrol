"""
 FastAPI Backend (Python): Serves the React frontend
CORSMiddleware: enables Cross-Origin Resource Sharing, allowing requests from other domains (e.g., a frontend on a different server). StaticFiles: used to serve static files (like a built React app).

to run fastapi app -> uvicorn test:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI() # Initializes a FastAPI application.

# Enable CORS so frontend can call API (from any origin (*), with any methods or headers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#It returns a simple JSON message to confirm the backend is running.
@app.get("/")
def root():
    return {"message": "Backend is alive!"}

# Serve React build (after building frontend)
app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
