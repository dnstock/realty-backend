from fastapi import FastAPI
from core import settings
from app.api import api_router, register_middleware, register_error_handlers
from . import print_startup_info

app = FastAPI()

# Register error handlers
register_error_handlers(app)

# Register middleware
register_middleware(app)

# Register API routes
app.include_router(api_router, prefix="/api")

# Run when the application starts
# Array of key-value pairs to display
print_startup_info([
    ('Application Name', settings.app_name),
    ('Environment', settings.app_env),
    ('Debug Mode', str(settings.app_debug)),
    ('Docked', str(settings.app_is_docked)),
    ('Log Directory', f'./{settings.log_dir}/'),
    ('Log Level', settings.log_level),
    ('SQL Query Logging', str(settings.sqlalchemy_echo)),
])
