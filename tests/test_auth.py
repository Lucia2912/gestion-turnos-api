def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "password123"
    })
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client):
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "email": "noexiste@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401