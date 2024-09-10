import os
from pathlib import Path
from typing import Optional, Literal
from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import BaseSettings

APP_DIR = Path(__file__).resolve().parent.parent  # ./backend/app/
ROOT_DIR = APP_DIR.parent                         # ./backend/

# Check if the app is running in a Docker container
is_docker_env = Path('/.dockerenv').exists() or (
    (cgroup_file := Path('/proc/self/cgroup')).is_file() and 'docker' in cgroup_file.read_text()
)

# Add default .env file and environment-specific .env file if it exists
env_specific_file = ROOT_DIR / 'envs' / f'.env.{os.getenv('ENVIRONMENT')}'
env_files = (ROOT_DIR / 'envs' / '.env',)
if Path(env_specific_file).is_file():
    env_files += (env_specific_file,)
    
class Settings(BaseSettings):
    # Application and Server Configuration
    app_name: str = Field(..., description='The name of the application')
    app_host: str = Field(..., description='The host the application is running on')
    app_port: int = Field(..., description='The port the application is running on')
    app_env: str = Field(..., description='The environment the application is running in')
    app_debug: bool = Field(False, description='The debug mode of the application')
    app_is_docked: bool = is_docker_env
    
    # Database Configuration
    postgres_user: str = Field(..., description='Postgres database user')
    postgres_password: str = Field(..., description='Postgres database password')
    postgres_host: str = Field(..., description='Postgres database host')
    postgres_port: int = Field(..., description='Postgres database port')
    postgres_db: str = Field(..., description='Postgres database name')
    postgres_test_db: str = Field(..., description='Postgres test database name')
    postgres_pool_size: int = Field(10, description='Postgres database pool size')
    postgres_max_overflow: int = Field(20, description='Postgres database max overflow')
    postgres_pool_timeout: int = Field(30, description='Postgres database pool timeout')
    postgres_debug_log_queries: Optional[bool] = Field(None, description='Log SQL queries for debugging')
    postgres_url: str = ''
    postgres_test_url: str = ''
    sqlalchemy_future: bool = True  # Use the latest features and deprecations
    sqlalchemy_echo: bool = False  # Implementation of postgres_log_queries
    
    # JWT and Security Configuration
    jwt_secret_key: str = Field(..., description='JWT secret')
    jwt_algorithm: str = Field(..., description='JWT algorithm')
    jwt_access_token_expire_minutes: int = Field(..., description='JWT access token expiry time in minutes')
    jwt_refresh_token_expire_days: int = Field(..., description='JWT refresh token expiry time in days')
    # jwt_reset_password_token_expire_minutes: int = Field(..., description='JWT reset password token expiry time in minutes')
    # jwt_verify_email_token_expire_minutes: int = Field(..., description='JWT verify email token expiry time in minutes')
    
    # API Configuration
    api_cors_origins: list[str] = Field(..., description='List of allowed origins')
    api_v1_cors_origins: Optional[list[str]] = Field(None, description='List of allowed origins specific for v1 API')
    
    # Redis or Cache Configuration
    redis_host: str = Field(..., description='Redis server hostname or IP address')
    redis_port: int = Field(6379, description='Redis server port')
    redis_db: int = Field(0, description='Redis database index')
    redis_cache_db: int = Field(1, description='Redis cache database index')
    redis_db_url: str = ''
    redis_cache_url: str = ''
    
    # Email Configuration
    smtp_server: Optional[str] = Field(None, description='Email host')
    smtp_port: Optional[str] = Field(None, description='Email port')
    smtp_user: Optional[str] = Field(None, description='Email user')
    smtp_password: Optional[str] = Field(None, description='Email password')
    
    # Logging Configuration
    log_dir: str = Field('logs', description='The log directory of the application')
    log_file: str = Field('app.log', description='The log file of the application')
    log_level: str = Field('INFO', description='The log level of the application')
    log_level_file: Optional[str] = Field(None, description='The log level for the log file (optional)')
    log_level_console: Optional[str] = Field(None, description='The log level for the console (optional)')
    log_max_files: int = Field(5, description='The max log files to store')
    log_max_file_size_bytes: int = Field(5242880, description='The max file size in bytes for each log file')
    log_format: Literal['text', 'json'] = Field('text', description='The log formatter to use (text or json)')
    log_format_file: Optional[Literal['text', 'json']] = Field(None, description='The log formatter for the log file (optional)')
    log_format_console: Optional[Literal['text', 'json']] = Field(None, description='The log formatter for the console (optional)')
    
    # Alerts Configuration
    alerts_email_enabled: bool = Field(False, description='Enable email alerts')
    alerts_email_from: Optional[str] = Field(None, description='Email address to send alerts from')
    alerts_email_to: Optional[str] = Field(None, description='Email address to send alerts to')
    alerts_sms_enabled: Optional[bool] = Field(False, description='Enable SMS alerts')
    alerts_slack_enabled: Optional[bool] = Field(False, description='Enable Slack alerts')

    # Possible future settings
    # app_version: str = Field(..., description='The version of the application')
    # app_port: int = Field(..., description='The port the application is running on')
    # app_host: str = Field(..., description='The host the application is running on')
    # app_url: str = Field(..., description='The URL of the application', exclude=True)
    # app_key: str = Field(..., description='The key of the application')
    # app_debug: bool = Field(False, description='The debug mode of the application')
    # app_log_level: str = Field(..., description='The log level of the application')
    # app_log_file: str = Field(..., description='The log file of the application')
    # app_log_format: str = Field(..., description='The log format of the application')
    # app_log_date_format: str = Field(..., description='The log date format of the application')
    # app_log_max_files: int = Field(..., description='The log max files of the application')
    # app_log_max_size: int = Field(..., description='The log max size of the application')
    # app_timezone: str = Field(..., description='The timezone of the application')
    # app_locale: str = Field(..., description='The locale of the application')
    # app_fallback_locale: str = Field(..., description='The fallback locale of the application')
    # app_frontend_url: str = Field(..., description='The frontend URL of the application')
    # app_frontend_port: int = Field(..., description='The frontend port of the application')
    # app_frontend_api_url: str = Field(..., description='The frontend API URL of the application')
    # app_frontend_api_version: str = Field(..., description='The frontend API version of the application')

    model_config = {
        'env_file': env_files,
        'env_file_encoding': 'utf-8',
        'case_sensitive': False,
        # 'validate_default': True,
    }

    # Adjust hostnames if running in Docker container
    @field_validator('postgres_host', 'redis_host', mode='before')
    def adjust_hostnames(self, v: str) -> str:
        if v == 'localhost' and is_docker_env:
            return 'host.docker.internal'
        return v

    # Set the SQLAlchemy echo flag
    @field_validator('sqlalchemy_echo', mode='after')
    def set_sqlalchemy_echo(self, v: bool | None, info: ValidationInfo) -> bool:
        values = info.data
        if values['postgres_debug_log_queries'] is None:
            # Default to True in development
            return values['app_env'] == 'development'
        else:
            # Set to value of environment variable, if defined
            return values['postgres_debug_log_queries']
    
    # Uppercase the log levels
    @field_validator('log_level', 'log_level_file', 'log_level_console', mode='before')
    def ensure_uppercase_log_levels(self, v: str | None, info: ValidationInfo) -> str:
        values = info.data
        return values['log_level'].upper() if v is None else v.upper()
    
    # Set the log formats
    @field_validator('log_format', 'log_format_file', 'log_format_console', mode='after')
    def set_log_formats(self, v: str | None, info: ValidationInfo) -> str:
        values = info.data
        return values['log_format'].lower() if v is None else v.lower()
    
    # Construct the database URLs
    @field_validator('postgres_url', 'postgres_test_url', mode='after')
    def construct_database_urls(self, v: str | None, info: ValidationInfo) -> str:
        values = info.data
        base_url = (
            f"postgresql://{values['postgres_user']}:{values['postgres_password']}"
            f"@{values['postgres_host']}:{values['postgres_port']}/"
        )
        if info.field_name == 'postgres_test_url':
            return base_url + values['postgres_test_db']
        return base_url + values['postgres_db']
    
    # Construct the Redis URLs
    @field_validator('redis_db_url', 'redis_cache_url', mode='after')
    def adjust_redis_host_and_url(self, v: str | None, info: ValidationInfo) -> str:
        values = info.data
        base_url = f'redis://{values["redis_host"]}:{values["redis_port"]}/'
        if info.field_name == 'redis_cache_url':
            return base_url + str(values['redis_cache_db'])
        return base_url + str(values['redis_db'])

# Initialize settings
settings = Settings()  # type: ignore (values will be set by env variables)
