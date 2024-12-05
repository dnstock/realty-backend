#
# Description: Middleware for API v1 exclusively
#
# For global or general middleware settings see: app/core/middleware.py
#
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core import settings

# Specific CORS settings for API v1
def v1_cors_middleware(app: FastAPI) -> None:
    # Only add this if the environment variable is set
    if(settings.api_v1_cors_origins is not None):
        app.add_middleware(CORSMiddleware,
            allow_origins=settings.api_v1_cors_origins,
            allow_methods=['*'],
            allow_headers=['*'],
        )
