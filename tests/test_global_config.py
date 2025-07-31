from unittest.mock import patch
from pydantic_settings import SettingsConfigDict
import pytest
from pydantic import ValidationError
from src.config import DBSettings
import os

def test_settings_load_env():
    with patch.dict(os.environ, {
        "DB_USER": "testuser",
        "DB_PASSWORD": "testpass",
        "DB_HOST": "db",
        "DB_PORT": "5432",
        "DB_NAME": "prod",
        "DB_URL": "postgresql+psycopg2://testuser:testpass@db:5432/prod"
    }):
        settings = DBSettings()

        assert settings.user == "testuser"
        assert settings.password == "testpass"
        assert settings.host == "db"
        assert settings.port == 5432
        assert settings.name == "prod"
        assert str(settings.url) == "postgresql+psycopg2://testuser:testpass@db:5432/prod"