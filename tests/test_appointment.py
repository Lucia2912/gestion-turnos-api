from datetime import datetime, timedelta, timezone

def get_token(client, email="client@test.com", password="password123"):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]

def future_appointment():
    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=1)
    return {"provider_id": 2, "start_time": start.isoformat(), "end_time": end.isoformat()}

# --- Crear turno ---
def test_create_appointment_success(client):
    token = get_token(client)
    response = client.post("/appointments/",
        json=future_appointment(),
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"

def test_create_appointment_unauthorized(client):
    response = client.post("/appointments/", json=future_appointment())
    assert response.status_code == 401

def test_create_appointment_overlap(client):
    token = get_token(client)
    data = future_appointment()
    client.post("/appointments/", json=data, headers={"Authorization": f"Bearer {token}"})
    response = client.post("/appointments/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409

# --- Cancelar turno ---
def test_cancel_appointment_success(client):
    token = get_token(client)
    create = client.post("/appointments/",
        json=future_appointment(),
        headers={"Authorization": f"Bearer {token}"}
    )
    appointment_id = create.json()["id"]
    response = client.patch(f"/appointments/{appointment_id}/cancel",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"

def test_cancel_appointment_not_owner(client):
    # client1 crea el turno
    token1 = get_token(client, "client1@test.com")
    create = client.post("/appointments/",
        json=future_appointment(),
        headers={"Authorization": f"Bearer {token1}"}
    )
    appointment_id = create.json()["id"]

    # client2 intenta cancelarlo
    token2 = get_token(client, "client2@test.com")
    response = client.patch(f"/appointments/{appointment_id}/cancel",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403