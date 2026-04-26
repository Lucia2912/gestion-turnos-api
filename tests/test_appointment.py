from datetime import datetime, timedelta, timezone

def get_token(client, email="client@test.com", password="password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]

def future_appointment(provider_id):
    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=1)
    return {"provider_id": provider_id, "start_time": start.isoformat(), "end_time": end.isoformat()}

def test_create_appointment_success(client, provider_id):
    token = get_token(client)
    response = client.post("/appointments/",
        json=future_appointment(provider_id),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"

def test_create_appointment_overlap(client, provider_id):
    token = get_token(client)
    data = future_appointment(provider_id)
    client.post("/appointments/", json=data, headers={"Authorization": f"Bearer {token}"})
    response = client.post("/appointments/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409

def test_cancel_appointment_success(client, provider_id):
    token = get_token(client)
    create = client.post("/appointments/",
        json=future_appointment(provider_id),
        headers={"Authorization": f"Bearer {token}"}
    )
    appointment_id = create.json()["id"]
    response = client.patch(f"/appointments/{appointment_id}/cancel",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"

def test_cancel_appointment_not_owner(client, provider_id):
    token1 = get_token(client, "client1@test.com")
    create = client.post("/appointments/",
        json=future_appointment(provider_id),
        headers={"Authorization": f"Bearer {token1}"}
    )
    appointment_id = create.json()["id"]
    token2 = get_token(client, "client2@test.com")
    response = client.patch(f"/appointments/{appointment_id}/cancel",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403

def test_create_appointment_invalid_provider(client):
    token = get_token(client)
    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=1)
    response = client.post("/appointments/",
        json={"provider_id": 999, "start_time": start.isoformat(), "end_time": end.isoformat()},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Provider not found"

def test_create_appointment_with_non_provider_user(client):
    # Registrar otro client e intentar usarlo como provider
    token1 = get_token(client, "client1@test.com")
    token2 = get_token(client, "client2@test.com")
    
    # Obtener el id del client2 logueándose
    login = client.post("/auth/login", json={"email": "client2@test.com", "password": "password123"})
    
    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=1)
    
    response = client.post("/appointments/",
        json={"provider_id": 2, "start_time": start.isoformat(), "end_time": end.isoformat()},
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User is not a provider"