from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.appointment import AppointmentStatus

class AppointmentCreate(BaseModel):
    provider_id: int
    start_time: datetime
    end_time: datetime

class AppointmentOut(BaseModel):
    id: int
    client_id: int
    provider_id: int
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus

    model_config = ConfigDict(from_attributes=True)
