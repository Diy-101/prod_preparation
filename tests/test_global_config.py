import pytest
from src.config import DBSettings, AuthSettings


def test_settings_load_env():
        settings = DBSettings()

        assert settings.user == "testuser"
        assert settings.password == "testpass"
        assert settings.host == "db"
        assert settings.port == 5432
        assert settings.name == "prod"
        assert str(settings.url) == "postgresql+psycopg2://testuser:testpass@db:5432/prod"

        settings = AuthSettings()
        assert settings.algorithm == "HS256"
        assert settings.token_time_minutes_expiration == 30