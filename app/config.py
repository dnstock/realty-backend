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
    database_user: str = os.getenv('DATABASE_USER')
    database_password: str = os.getenv('DATABASE_PASSWORD')
    database_name: str = os.getenv('DATABASE_NAME')
    database_host: str = os.getenv('DATABASE_HOST', 'localhost')
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')
    access_token_expire_minutes: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    database_url: str = f"postgresql://{database_user}:{database_password}@{database_host}/{database_name}"

settings = Settings()
