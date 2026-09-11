from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def register_user(username, email, password):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


def login_user(username, password):
    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )
    return response.json()["access_token"]


def test_register_user():
    response = register_user(
        "testuser19",
        "testuser19@example.com",
        "Test@123"
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


def test_task_crud():
    username = "cruduser19"
    email = "cruduser19@example.com"
    password = "Crud@123"

    register_user(username, email, password)

    token = login_user(username, password)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing CRUD operations"
        },
        headers=headers
    )

    assert create_response.status_code == 201

    task = create_response.json()
    task_id = task["id"]

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=headers
    )

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Test Task"

    update_response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated Test Task",
            "completed": True
        },
        headers=headers
    )

    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=headers
    )

    assert delete_response.status_code == 200


def test_idor_protection():
    user1 = "owner19"
    user2 = "attacker19"

    register_user(
        user1,
        "owner19@example.com",
        "Owner@123"
    )

    register_user(
        user2,
        "attacker19@example.com",
        "Attacker@123"
    )

    token1 = login_user(user1, "Owner@123")
    token2 = login_user(user2, "Attacker@123")

    create_response = client.post(
        "/tasks",
        json={
            "title": "Private Task",
            "description": "Only owner can access this"
        },
        headers={
            "Authorization": f"Bearer {token1}"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    attack_response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token2}"
        }
    )

    assert attack_response.status_code == 404
    assert attack_response.json()["detail"] == "Task not found or access denied"
