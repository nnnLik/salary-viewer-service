from httpx import AsyncClient


async def test_registration_correct(ac: AsyncClient):
    response = await ac.post(
        "/auth/jwt/register",
        json={
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], str)
    assert data["email"] == "user@example.com"
    assert data["is_active"] == True
    assert data["is_superuser"] == False
    assert data["is_verified"] == False


async def test_registration_incorrect(ac: AsyncClient):
    response = await ac.post(
        "/auth/jwt/register",
        json={
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "REGISTER_USER_ALREADY_EXISTS"


async def test_login_with_correct_credentials(ac: AsyncClient):
    response = await ac.post(
        "/auth/jwt/login",
        data={
            "grant_type": "",
            "username": "user@example.com",
            "password": "string",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_with_incorrect_credentials(ac: AsyncClient):
    response = await ac.post(
        "/auth/jwt/login",
        data={
            "grant_type": "",
            "username": "user@example.com",
            "password": "incorrect_password",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "LOGIN_BAD_CREDENTIALS"
