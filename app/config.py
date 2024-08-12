from pydantic import ValidationError
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load the base .env file
load_dotenv(".env")

# Load the environment-specific .env file
env = os.getenv('ENVIRONMENT', 'development')
env_specific = f".env.{env}"
load_dotenv(env_specific)

class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_name: str
    database_host: str = 'localhost'
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str
    
    @classmethod
    def validate_env_vars(cls):
        required_vars = [
            'DATABASE_USER', 'DATABASE_PASSWORD', 'DATABASE_NAME', 
            'SECRET_KEY', 'ALGORITHM', 'ACCESS_TOKEN_EXPIRE_MINUTES'
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValidationError(f"Missing required environment variables: {', '.join(missing_vars)}")

    def __init__(self, **kwargs):
        self.validate_env_vars()
        super().__init__(**kwargs)
        self.database_url = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

# Initialize settings
settings = Settings()
