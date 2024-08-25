from pydantic import Field, model_validator
from pydantic_settings import BaseSettings
import os

# Absolute path of `configs` directory relative to this file
env_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'envs'))

class Settings(BaseSettings):
    environment: str = Field(..., description="The environment type (development, production, etc.)")
    database_user: str = Field(..., description="Database user")
    database_password: str = Field(..., description="Database password")
    database_name: str = Field(..., description="Database name")
    database_host: str = Field('localhost', description="Database host")
    database_port: int = Field(5432, description="Database port")
    secret_key: str = Field(..., description="Secret key for JWT")
    algorithm: str = Field(..., description="Algorithm for JWT")
    access_token_expire_minutes: int = Field(..., description="Access token expiry time in minutes")
    database_url: str = Field('', description="Database URL", exclude=True)
    is_docker: bool = Field(False, description="Set to True if running in Docker")
    
    model_config = {
        'env_file': [
            os.path.join(env_file_path, ".env"),
            os.path.join(env_file_path, f".env.{os.getenv('ENVIRONMENT')}")
        ],
        'env_file_encoding': 'utf-8',
        'case_sensitive': False,
        # 'validate_default': True,
    }
    
    @model_validator(mode='after')
    def adjust_database_host_and_url(cls, values):
        # Adjust database_host if running in Docker
        if values.database_host == 'localhost' and values.is_docker:
            values.database_host = 'host.docker.internal'
        
        # Assemble the database URL
        values.database_url = (
            f"postgresql://{values.database_user}:{values.database_password}"
            f"@{values.database_host}:{values.database_port}/{values.database_name}"
        )
        
        return values

# Initialize settings
settings = Settings()
