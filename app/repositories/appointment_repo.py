from sqlalchemy.orm import Session
from app.models.appointment import Appointment

def create_appointment(db: Session, appointment: Appointment):
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_overlapping_appointments(db: Session, provider_id: int, start_time: str, end_time: str):
    return db.query(Appointment).filter(
        Appointment.provider_id == provider_id,
        Appointment.start_time < end_time,
        Appointment.end_time > start_time,
        Appointment.status == "scheduled"
    ).all()
