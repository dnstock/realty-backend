from fastapi import FastAPI
from core import settings, utils
from api import api_router, register_middleware, register_error_handlers
import platform

app = FastAPI()

# Register error handlers
register_error_handlers(app)

# Register middleware
register_middleware(app)

# Register API routes
app.include_router(api_router, prefix='/api')

app_info = [
    ('Application Name', settings.app_name),
    ('Environment', settings.app_env),
    ('Debug Mode', str(settings.app_debug)),
    ('Docked', str(settings.app_is_docked)),
    ('Log Directory', f'./{settings.log_dir}/'),
    ('Log Level', settings.log_level),
    ('SQL Query Logging', str(settings.sqlalchemy_echo)),
]

system_info = [
    ('Python Version', platform.python_version()),
]

# Run when the application starts
utils.print_boxed_sections(app_info, system_info, title='Application Information')
