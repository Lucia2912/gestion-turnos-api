from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.appointment import AppointmentCreate
from app.services.appointment_service import  create_appointment_service
from app.core.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    new_appointment = create_appointment_service(db, client_id = user_id, 
    provider_id = appointment.provider_id,
    start_time = appointment.start_time, 
    end_time = appointment.end_time)
    return new_appointment