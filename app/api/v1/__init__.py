from types import ModuleType
from fastapi import FastAPI, APIRouter
from .errors import *
from .middleware import *
from .endpoints import auth, users, properties, buildings, units, leases, tenants, insurances

router = APIRouter()

modules: list[ModuleType] = [auth, users, properties, buildings, units, leases, tenants, insurances]

for module in modules:
    module_name: str = module.__name__.split('.')[-1]  # Get the module name without the package name
    router.include_router(getattr(module, 'router', APIRouter()), prefix=f'/{module_name}', tags=[module_name])

# Register middleware for API v1
def register_middleware(app: FastAPI) -> None:
    v1_cors_middleware(app)

# Register error handlers for API v1
def register_error_handlers(app: FastAPI) -> None:
    v1_http_exception_handler(app)
    v1_unhandled_exception_handler(app)

__all__ = [
    'router',
    'register_middleware',
    'register_error_handlers'
]
