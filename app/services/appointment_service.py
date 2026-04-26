from app.repositories.appointment_repo import create_appointment, get_overlapping_appointments, update_appointment_status, get_appointment_by_id
from app.models.appointment import Appointment, AppointmentStatus
from fastapi import HTTPException

#Crea un nuevo turno
def create_appointment_service(db, client_id, provider_id, start_time, end_time):
    #Controla que no exista otro turno en el mismo horario
    overlapping = get_overlapping_appointments(
        db, 
        provider_id, 
        start_time, 
        end_time
    )
    if overlapping:
        raise HTTPException(status_code=409, detail="Overlapping appointments found")
    appointment = Appointment(client_id = client_id, provider_id = provider_id,
        start_time = start_time,
        end_time = end_time)
    return create_appointment(db, appointment)

#Cancelo turno
def cancel_appointment_service(db, appointment_id: int, user_id: int):
    appointment = get_appointment_by_id(db, appointment_id)
    if appointment.client_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if appointment.status == AppointmentStatus.cancelled:
        raise HTTPException(status_code=400, detail="Appointment already cancelled")
    if appointment.status == AppointmentStatus.completed:
        raise HTTPException(status_code=400, detail="Cannot cancel a completed appointment")
    return update_appointment_status(db, appointment_id, AppointmentStatus.cancelled)

#Confirma turno
def confirm_appointment_service(db, appointment_id: int, user_id: int):
    appointment = get_appointment_by_id(db, appointment_id)
    if appointment.provider_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if appointment.status != AppointmentStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending appointments can be confirmed")
    return update_appointment_status(db, appointment_id, AppointmentStatus.confirmed)
