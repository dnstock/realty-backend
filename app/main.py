from fastapi import FastAPI
from core import settings
from app.api import api_router, register_middleware, register_error_handlers

app = FastAPI()

# Register error handlers
register_error_handlers(app)

# Register middleware
register_middleware(app)

# Register API routes
app.include_router(api_router, prefix="/api")

# Run when the application starts
def start_app():
    print(f"App name: {settings.app_name}")
    print(f"Postgres URL: {settings.postgres_url}")

# Entry point for the application
if __name__ == "__main__":
    start_app()
