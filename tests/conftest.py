import pytest
from fastapi.testclient import TestClient
from src.database import get_db
from main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def db():
    with get_db() as db:
        yield db

@pytest.fixture(scope="module")
def user():
    return {
        "login": "yellowMonkey",
        "email": "yellowstone1980@you.ru",
        "password": "jdfiwIUG31213#$",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+74951239922",
        "image": "https://http.cat/images/100.jpg"
    }