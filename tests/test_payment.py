from unittest.mock import patch
from datetime import datetime, timedelta, timezone

def get_token(client, email="client@test.com"):
    client.post("/auth/register", json={"email": email, "password": "password123"})
    response = client.post("/auth/login", json={"email": email, "password": "password123"})
    return response.json()["access_token"]

# test_payment.py
def create_appointment(client, token, provider_id):
    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=1)
    response = client.post("/appointments/",
        json={"provider_id": provider_id, "start_time": start.isoformat(), "end_time": end.isoformat()},
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()["id"]

def test_payment_approved(client, provider_id):
    token = get_token(client)
    appointment_id = create_appointment(client, token, provider_id)
    with patch("app.services.payment_service.PaymentService._simulate_gateway") as mock:
        mock.return_value = {"status": "approved", "transaction_id": "TXN-1234", "message": "Payment approved"}
        response = client.post(f"/appointments/{appointment_id}/pay",
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json()["status"] == "approved"

def test_payment_rejected(client, provider_id):
    token = get_token(client)
    appointment_id = create_appointment(client, token, provider_id)
    with patch("app.services.payment_service.PaymentService._simulate_gateway") as mock:
        mock.return_value = {"status": "rejected", "transaction_id": None, "message": "Insufficient funds"}
        response = client.post(f"/appointments/{appointment_id}/pay",
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"

def test_payment_already_paid(client, provider_id):
    token = get_token(client)
    appointment_id = create_appointment(client, token, provider_id)
    with patch("app.services.payment_service.PaymentService._simulate_gateway") as mock:
        mock.return_value = {"status": "approved", "transaction_id": "TXN-1234", "message": "Payment approved"}
        client.post(f"/appointments/{appointment_id}/pay",
            headers={"Authorization": f"Bearer {token}"}
        )
        response = client.post(f"/appointments/{appointment_id}/pay",
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 400

def test_payment_not_owner(client, provider_id):
    token1 = get_token(client, "client1@test.com")
    token2 = get_token(client, "client2@test.com")
    appointment_id = create_appointment(client, token1, provider_id)
    response = client.post(f"/appointments/{appointment_id}/pay",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403