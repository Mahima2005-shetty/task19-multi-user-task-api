from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser19",
            "email": "testuser19@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code in [201, 400]


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "mahima",
            "password": "Mahima@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_unauthorized_task_access():
    response = client.get("/tasks")

    assert response.status_code == 401
