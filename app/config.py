from pydantic import ValidationError
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Absolute path of `configs` directory relative to this file
configs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config'))

# Load the global .env file
load_dotenv(os.path.join(configs_dir, ".env"))

class Settings(BaseSettings):
    environment: str
    database_user: str
    database_password: str
    database_name: str
    database_host: str = 'localhost'
    database_port: int = 5432
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str = ''
    is_docker: bool = False  # Will be set to True if running in Docker
    
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
        # Load the environment-specific .env file
        env_file = f".env.{os.getenv('ENVIRONMENT')}"
        load_dotenv(os.path.join(configs_dir, env_file), override=True)
        
        # Validate environment
        self.validate_env_vars()
        super().__init__(**kwargs)
        
        # Set default database host for Docker
        if self.database_host == 'localhost' and self.is_docker:
            self.database_host = 'host.docker.internal'
        
        # Create the database URL
        self.database_url = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

# Initialize settings
settings = Settings()
