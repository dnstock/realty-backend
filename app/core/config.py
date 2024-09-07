from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os

APP_DIR = Path(__file__).resolve().parent.parent  # ./backend/app/
ROOT_DIR = APP_DIR.parent                         # ./backend/

# Add default .env file and environment-specific .env file if it exists
env_specific_file = ROOT_DIR / 'envs' / f'.env.{os.getenv('ENVIRONMENT')}'
env_files = (ROOT_DIR / 'envs' / '.env',)
if Path(env_specific_file).is_file():
    env_files += (env_specific_file,)
    
class Settings(BaseSettings):
    # Application and Server Settings
    app_name: str = Field(..., description='The name of the application')
    app_host: str = Field(..., description='The host the application is running on')
    app_port: int = Field(..., description='The port the application is running on')
    app_env: str = Field(..., description='The environment the application is running in')
    app_debug: bool = Field(False, description='The debug mode of the application')
    app_is_docked: bool = False
    
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
    
    # JWT and Security Settings
    jwt_secret_key: str = Field(..., description='JWT secret')
    jwt_algorithm: str = Field(..., description='JWT algorithm')
    jwt_access_token_expire_minutes: int = Field(..., description='JWT access token expiry time in minutes')
    jwt_refresh_token_expire_days: int = Field(..., description='JWT refresh token expiry time in days')
    # jwt_reset_password_token_expire_minutes: int = Field(..., description='JWT reset password token expiry time in minutes')
    # jwt_verify_email_token_expire_minutes: int = Field(..., description='JWT verify email token expiry time in minutes')
    
    # API settings
    api_cors_origins: list[str] = Field(..., description='List of allowed origins')
    api_v1_cors_origins: Optional[list[str]] = Field(None, description='List of allowed origins specific for v1 API')
    
    # Redis or Cache Settings
    redis_host: str = Field(..., description='Redis server hostname or IP address')
    redis_port: int = Field(6379, description='Redis server port')
    redis_db: int = Field(0, description='Redis database index')
    redis_cache_db: int = Field(1, description='Redis cache database index')
    redis_db_url: str = ''
    redis_cache_url: str = ''
    
    # Email settings (for future use)
    email_host: Optional[str] = Field(None, description='Email host')
    email_port: Optional[int] = Field(None, description='Email port')
    email_user: Optional[str] = Field(None, description='Email user')
    email_password: Optional[str] = Field(None, description='Email password')
    
    # Logging Configuration
    log_dir: str = Field('logs', description='The log directory of the application')
    log_file: str = Field('app.log', description='The log file of the application')
    log_level: str = Field('INFO', description='The log level of the application')
    log_max_files: int = Field(5, description='The max log files to store')
    log_max_file_size_bytes: int = Field(5242880, description='The max file size in bytes for each log file')
    log_format: str = Field('%(asctime)s - %(name)s - %(levelname)s - %(message)s', description='The message format for log files')

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

    # Check whether the app is running in a Docker container
    @field_validator('app_is_docked', mode='before')
    def set_app_is_docked(cls, value: bool | None) -> bool:
        path = '/proc/self/cgroup'
        return (
            Path('/.dockerenv').exists() or
            (Path(path).is_file() and any('docker' in line for line in Path(path).open()))
        )
        
    @field_validator('log_level', mode='before')
    def capitalize_log_level(cls, value: str) -> str:
        return value.upper()
    
    # Set the SQLAlchemy echo flag
    @field_validator('sqlalchemy_echo', mode='after')
    def set_sqlalchemy_echo(cls, v: bool | None, info: ValidationInfo) -> bool:
        values = info.data
        if values['postgres_debug_log_queries'] is None:
            # Default to True in development
            return values['app_env'] == 'development'
        else:
            # Set to `postgres_debug_log_queries` if defined
            return values['postgres_debug_log_queries']

    # Assemble the database URL and the test database URL
    @field_validator('postgres_url', 'postgres_test_url', mode='after')
    def adjust_database_host_and_url(cls, v: str | None, info: ValidationInfo) -> str:
        values = info.data
        # Adjust postgres_host if running in Docker
        if values['postgres_host'] == 'localhost' and values['app_is_docked']:
            values['postgres_host'] = 'host.docker.internal'
        
        # Construct URL
        url = (
            f'postgresql://{values['postgres_user']}:{values['postgres_password']}'
            f'@{values['postgres_host']}:{values['postgres_port']}/'
        )
        
        # Assign appropriate URLs
        values['postgres_url'] = url + values['postgres_db']
        values['postgres_test_url'] = url + values['postgres_test_db']
        
        # Return the updated URL for each field
        if v == values['postgres_url']:
            return values['postgres_url']
        return values['postgres_test_url']
    
    # Assembly the Redis URL and the Redis cache URL
    @field_validator('redis_db_url', 'redis_cache_url', mode='after')
    def adjust_redis_host_and_url(cls, v: str | None, info: ValidationInfo) -> str:
        values = info.data
        # Adjust redis_host if running in Docker
        if values['redis_host'] == 'localhost' and values['app_is_docked']:
            # Modify redis_host directly in the values dictionary
            values['redis_host'] = 'host.docker.internal'
        
        # Construct Redis URL
        url = f'redis://{values["redis_host"]}:{values["redis_port"]}/'
        
        # Assign the Redis DB URLs
        values['redis_db_url'] = url + str(values['redis_db'])
        values['redis_cache_url'] = url + str(values['redis_cache_db'])
        
        # Return the specific value being validated
        if v == values['redis_db_url']:
            return values['redis_db_url']
        return values['redis_cache_url']

# Initialize settings
settings = Settings()  # type: ignore (values will be set by env variables)
