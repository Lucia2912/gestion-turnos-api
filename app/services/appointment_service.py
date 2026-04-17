from app.repositories.appointment_repo import create_appointment, get_overlapping_appointments
from app.models.appointment import Appointment

def create_appointment_service(db, client_id, provider_id, start_time, end_time):
    # Check for overlapping appointments
    overlapping = get_overlapping_appointments(
        db, 
        provider_id, 
        start_time, 
        end_time
    )
    
    if overlapping:
        raise ValueError("Overlapping appointments found")
    
    # Create new appointment
    appointment = Appointment(client_id = client_id, provider_id = provider_id,
        start_time = start_time,
        end_time = end_time)
    return create_appointment(db, appointment)

