def test_registration(client, user):
    response = client.post(
        url="/api/auth/register",
        json=user,
    )
    assert response.status_code == 201, f"Response: {response.text}"
    response_data = response.json()["profile"]

    assert response_data == {
        "login": "yellowMonkey",
        "email": "yellowstone1980@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+74951239922",
        "image": "https://http.cat/images/100.jpg",
    }

def test_login(client, user):
    response = client.post(
        url="/api/auth/sign-in",
        json={
            "login": user["login"],
            "password": user["password"],
        },
    )

    assert response.status_code == 200, f"Response: {response.text}"
    token = response.json()["token"]
    assert token is not None
    return token

def test_get_me(client, user):
    token = test_login(client, user)
    response = client.get(
        url="/api/me/profile",
        headers={"Authorization": f"Bearer {token}"},
    )
    response_data = response.json()

    assert response.status_code == 200, f"Response: {response.text}"
    assert response_data == {
        "login": "yellowMonkey",
        "email": "yellowstone1980@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+74951239922",
        "image": "https://http.cat/images/100.jpg",
    }

def test_patch_me(client, user):
    token = test_login(client, user)
    response = client.patch(
        url="/api/me/profile",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": "+749512387372"},
    )
    response_data = response.json()

    assert response.status_code == 200, f"Response: {response.text}"
    assert response_data == {
        "login": "yellowMonkey",
        "email": "yellowstone1980@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+749512387372",
        "image": "https://http.cat/images/100.jpg",
    }

def test_patch_me_empty(client, user):
    token = test_login(client, user)
    response = client.patch(
        url="/api/me/profile",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )
    response_data = response.json()

    assert response.status_code == 200, f"Response: {response.text}"
    assert response_data == {
        "login": "yellowMonkey",
        "email": "yellowstone1980@you.ru",
        "countryCode": "RU",
        "isPublic": True,
        "phone": "+749512387372",
        "image": "https://http.cat/images/100.jpg",
    }