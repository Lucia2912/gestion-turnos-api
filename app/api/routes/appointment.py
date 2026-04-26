from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.services.appointment_service import  create_appointment_service, cancel_appointment_service, confirm_appointment_service
from app.core.dependencies import get_current_user, get_db, require_role
from app.models.user import UserRole
from app.models.appointment import Appointment
from app.services.payment_service import payment_service
from app.schemas.payment import PaymentOut

router = APIRouter()


@router.post("/", response_model=AppointmentOut)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db), current_user: dict = Depends(require_role(UserRole.client))):
    new_appointment = create_appointment_service(db, client_id = current_user["user_id"], 
    provider_id = appointment.provider_id,
    start_time = appointment.start_time, 
    end_time = appointment.end_time)
    return new_appointment

@router.patch("/{appointment_id}/cancel", response_model=AppointmentOut)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role(UserRole.client))):
    return cancel_appointment_service(db, appointment_id, current_user["user_id"])

@router.patch("/{appointment_id}/confirm", response_model=AppointmentOut)
def confirm_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role(UserRole.provider))):
    return confirm_appointment_service(db, appointment_id, current_user["user_id"])

@router.get("/", response_model=list[AppointmentOut])
def get_all_appointments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(UserRole.admin))
):
    return db.query(Appointment).all()

# Solo clients pueden pagar
@router.post("/{appointment_id}/pay", response_model=PaymentOut)
def pay_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role(UserRole.client))):
    return payment_service.process_payment(db, appointment_id, current_user["user_id"])