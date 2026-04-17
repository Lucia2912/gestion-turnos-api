from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.services.user_service import register_user
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.repositories.user_repo import get_user_by_email
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        return {"error": "Email already register"}
    db_user = register_user(db, user.email, user.password, "client")
    #access_token = create_access_token(data={"sub": db_user.email})
    #return {"access_token": access_token, "token_type": "bearer"}
    return db_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return {"error": "Invalid credentials"}
    access_token = create_access_token({"user_id": db_user.id, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}




