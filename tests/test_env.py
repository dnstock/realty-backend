import os
import pytest
from dotenv import load_dotenv

def test_load_env_development():
    # Set environment to development for this test
    os.environ['ENVIRONMENT'] = 'development'

    # Load the base and environment-specific .env files
    load_dotenv(".env")
    load_dotenv(".env.development")

    # Test common settings
    assert os.getenv('ALGORITHM') == "HS256"
    assert os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') == "30"

    # Test environment-specific settings
    assert os.getenv('DATABASE_USER') == "admin"
    assert os.getenv('DATABASE_NAME') == "realty"
    assert os.getenv('DATABASE_PASSWORD') is not None
    assert os.getenv('SECRET_KEY') is not None

@pytest.fixture(scope="function", autouse=True)
def reset_env():
    """Reset environment variables before each test."""
    yield
    for key in list(os.environ.keys()):
        if key.startswith("DATABASE_") or key in ["SECRET_KEY", "ENVIRONMENT"]:
            del os.environ[key]

def test_load_env_testing():
    # Set environment to testing for this test
    os.environ['ENVIRONMENT'] = 'testing'

    # Load the base and environment-specific .env files
    load_dotenv(".env")
    load_dotenv(".env.testing")

    # Test common settings
    assert os.getenv('ALGORITHM') == "HS256"
    assert os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') == "30"

    # Test environment-specific settings
    assert os.getenv('DATABASE_USER') is not None
    assert os.getenv('DATABASE_NAME') is not None
    assert os.getenv('DATABASE_PASSWORD') is not None
    assert os.getenv('SECRET_KEY') is not None
