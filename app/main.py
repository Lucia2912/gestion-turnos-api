from fastapi import FastAPI
from app.api.routes import auth
from app.api.routes import appointment
from contextlib import asynccontextmanager

#Temporal
from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.appointment import Appointment

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

app.include_router(appointment.router, prefix="/appointments", tags=["appointments"])