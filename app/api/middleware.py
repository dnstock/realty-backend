from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from core.config import settings

# CORS settings for the API
def cors_middleware(app: FastAPI) -> None:
    app.add_middleware(CORSMiddleware,
        allow_origins=settings.api_cors_origins,  # List of allowed origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
    )
