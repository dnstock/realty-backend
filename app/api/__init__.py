from fastapi import FastAPI, APIRouter
from .errors import *
from .middleware import *
from .v1 import router as v1_router

api_router = APIRouter()

# Include the v1 API routes
api_router.include_router(v1_router, prefix='/v1')

# Register middleware for the API
def register_middleware(app: FastAPI) -> None:
    cors_middleware(app)  # Must be first
    request_id_middleware(app)

    # Uncomment the lines below to include v1-specific middleware
    #from .v1 import register_middleware as register_v1_middleware
    #register_v1_middleware(app)

# Register error handlers for the API
def register_error_handlers(app: FastAPI) -> None:
    common_http_exception_handler(app)
    common_validation_exception_handler(app)
    common_sqlalchemy_exception_handler(app)
    common_unhandled_exception_handler(app)

    # Uncomment the lines below to include v1-specific error handlers
    #from .v1 import register_error_handlers as register_v1_error_handlers
    #register_v1_error_handlers(app)

__all__ = [
    'api_router',
    'register_middleware',
    'register_error_handlers'
]
