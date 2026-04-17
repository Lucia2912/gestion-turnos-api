from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    client = "client"
    provider = "provider"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.client)
