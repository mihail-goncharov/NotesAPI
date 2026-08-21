from fastapi.testclient import TestClient


def test_register(client: TestClient):
    response = client.post(
        "/register", json={"email": "user2@gmail.com", "password": "123456789"}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["email"] == "user2@gmail.com"


def test_duplicate_email(client: TestClient):
    response = client.post(
        "/register", json={"email": "user@example.com", "password": "12345678"}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["email"] == "user@example.com"

    response = client.post(
        "/register", json={"email": "user@example.com", "password": "12345678"}
    )

    assert response.status_code == 409


def test_login_wrong_password(client: TestClient):
    client.post("/register", json={"email": "user@example.com", "password": "12345678"})

    response = client.post(
        "/login", json={"email": "user@example.com", "password": "1234567"}
    )

    assert response.status_code == 401
