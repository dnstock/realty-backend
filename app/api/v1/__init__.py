from fastapi import FastAPI, APIRouter
from .errors import *
from .middleware import *
from .endpoints import auth, users, properties, buildings, units, leases, tenants, insurances

router = APIRouter()

# Register routes for API v1
for module in [auth, users, properties, buildings, units, leases, tenants, insurances]:
    router.include_router(getattr(module, 'router'), prefix=f"/{module.__name__}", tags=[module.__name__])
    
# Register middleware for API v1
def register_middleware(app: FastAPI) -> None:
    v1_cors_middleware(app)

# Register error handlers for API v1
def register_error_handlers(app: FastAPI) -> None:
    v1_http_exception_handler(app)
    v1_unhandled_exception_handler(app)

__all__ = [
    "router",
    "register_middleware",
    "register_error_handlers"
]
