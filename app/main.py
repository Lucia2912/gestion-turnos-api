from fastapi import FastAPI
from app.api.routes import auth
from app.api.routes import appointment

#Temporal
from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.appointment import Appointment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Turnos api", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])

app.include_router(appointment.router, prefix="/appointments", tags=["appointments"])