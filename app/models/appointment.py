from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    provider_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="scheduled")

