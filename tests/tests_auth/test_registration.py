import json

from fastapi.testclient import TestClient
from main import app

client = TestClient(app, base_url="http://localhost:8080/api")

def test_registration():
    response = client.post(
        url="/auth/registration",
        content=json.dumps(
            {
                "login": "yellowMonkey",
                "email": "yellowstone1980@you.ru",
                "countryCode": "RU",
                "isPublic": True,
                "phone": "+74951239922",
                "image": "https://http.cat/images/100.jpg"
            }
        ),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    response_data = response.json()["profile"]

    assert response_data["login"] == "yellowMonkey"
    assert response_data["email"] == "yellowstone1980@you.ru"
    assert response_data["countryCode"] == "RU"
    assert response_data["isPublic"] is True
    assert response_data["phone"] == "+74951239922"
    assert response_data["image"] == "https://http.cat/images/100.jpg"