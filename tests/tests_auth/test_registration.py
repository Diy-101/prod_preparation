import pytest

def test_registration(client, test_user):
    response = client.post(
        url="/api/auth/register",
        json=test_user,
    )
    assert response.status_code == 201, f"Response: {response.text}"
    response_data = response.json()["profile"]

    assert response_data["login"] == "yellowMonkey"
    assert response_data["email"] == "yellowstone1980@you.ru"
    assert response_data["countryCode"] == "RU"
    assert response_data["isPublic"] is True
    assert response_data["phone"] == "+74951239922"
    assert response_data["image"] == "https://http.cat/images/100.jpg"

def test_login(client, test_user):
    response = client.post(
        url="/api/auth/sign-in",
        json={
            "login": test_user["login"],
            "password": test_user["password"],
        },
    )

    assert response.status_code == 200, f"Response: {response.text}"
    token = response.json()["token"]
    assert token is not None
    return token

def test_get_me(client, test_user):
    token = test_login(client, test_user)
    response = client.get(
        url="/api/me/profile",
        headers={"Authorization": f"Bearer {token}"},
    )
    response_data = response.json()

    assert response.status_code == 200, f"Response: {response.text}"
    assert response_data["email"] == test_user["email"]
    assert response_data["phone"] == test_user["phone"]
    assert response_data["countryCode"] == test_user["countryCode"]
    assert response_data["isPublic"] == test_user["isPublic"]
    assert response_data["image"] == test_user["image"]
    assert response_data["login"] == test_user["login"]