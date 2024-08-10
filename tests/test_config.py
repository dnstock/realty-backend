import os
import pytest
from app.config import Settings

def test_settings_loading():
    # Set environment to development for this test
    os.environ['ENVIRONMENT'] = 'development'

    # Load settings
    settings = Settings()

    # Test common settings
    assert settings.algorithm == "HS256"
    assert settings.access_token_expire_minutes == 30

    # Test environment-specific settings
    assert settings.database_user == "admin"
    assert settings.database_name == "realty"
    assert settings.database_password is not None
    assert settings.secret_key is not None

@pytest.fixture(scope="function", autouse=True)
def reset_env():
    """Reset environment variables before each test."""
    yield
    for key in list(os.environ.keys()):
        if key.startswith("DATABASE_") or key in ["SECRET_KEY", "ENVIRONMENT"]:
            del os.environ[key]

def test_settings_loading_testing():
    # Set environment to testing for this test
    os.environ['ENVIRONMENT'] = 'testing'

    # Load settings
    settings = Settings()

    # Test common settings
    assert settings.algorithm == "HS256"
    assert settings.access_token_expire_minutes == 30

    # Test environment-specific settings
    assert settings.database_user is not None
    assert settings.database_name is not None
    assert settings.database_password is not None
    assert settings.secret_key is not None