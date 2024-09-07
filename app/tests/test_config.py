from core import settings

def test_settings_loading():
    # Check that `settings` is loaded
    assert settings.app_env is not None
    assert settings.postgres_url != ''
    assert settings.postgres_test_url != ''
