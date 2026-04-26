from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from fastapi import HTTPException
from app.models.appointment import AppointmentStatus

#Agrega la logica de persistencia
def create_appointment(db: Session, appointment: Appointment):
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

#Control de turnos superpuestos
def get_overlapping_appointments(db: Session, provider_id: int, start_time: str, end_time: str):
    return db.query(Appointment).filter(
        Appointment.provider_id == provider_id,
        Appointment.start_time < end_time,
        Appointment.end_time > start_time,
        Appointment.status != AppointmentStatus.cancelled
    ).first()

#Busco turno por id
def get_appointment_by_id(db, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

#Cambio de estado del turno
def update_appointment_status(db, appointment_id: int, new_status: AppointmentStatus):
    appointment = get_appointment_by_id(db, appointment_id)
    appointment.status = new_status
    db.commit()
    db.refresh(appointment)
    return appointment