import random
from fastapi import HTTPException
from app.models.appointment import AppointmentStatus
from app.repositories.appointment_repo import get_appointment_by_id, update_appointment_status
from app.celery.tasks import send_confirmation_email

class PaymentService:
    def process_payment(self, db, appointment_id: int, user_id: int) -> dict:
        appointment = get_appointment_by_id(db, appointment_id)
        if appointment.client_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        if appointment.status != AppointmentStatus.pending:
            raise HTTPException(status_code=400, detail="Only pending appointments can be paid")
        # Simulación de pasarela de pagos
        payment_result = self._simulate_gateway()
        if payment_result["status"] == "approved":
            update_appointment_status(db, appointment_id, AppointmentStatus.confirmed)
            # Disparar email async
            send_confirmation_email.delay(user_id, appointment_id)
        return payment_result

    def _simulate_gateway(self) -> dict:
        # Simula distintos escenarios reales
        scenarios = [
            {"status": "approved", "transaction_id": f"TXN-{random.randint(1000, 9999)}", "message": "Payment approved"},
            {"status": "rejected", "transaction_id": None, "message": "Insufficient funds"},
            {"status": "error", "transaction_id": None, "message": "Gateway timeout"},
        ]
        # 70% aprobado, 20% rechazado, 10% error
        return random.choices(scenarios, weights=[70, 20, 10])[0]

payment_service = PaymentService()