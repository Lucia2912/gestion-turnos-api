from app.celery.worker import celery_app

@celery_app.task
def send_confirmation_email(user_id: int, appointment_id: int):
    # Por ahora simulamos el envío con un log
    print(f"Sending confirmation email to user {user_id} for appointment {appointment_id}")
    return {"status": "email_sent", "user_id": user_id, "appointment_id": appointment_id}

@celery_app.task
def send_cancellation_email(user_id: int, appointment_id: int):
    print(f"Sending cancellation email to user {user_id} for appointment {appointment_id}")
    return {"status": "email_sent", "user_id": user_id, "appointment_id": appointment_id}

@celery_app.task
def send_reminder_email(user_id: int, appointment_id: int):
    print(f"Sending reminder email to user {user_id} for appointment {appointment_id}")
    return {"status": "email_sent", "user_id": user_id, "appointment_id": appointment_id}