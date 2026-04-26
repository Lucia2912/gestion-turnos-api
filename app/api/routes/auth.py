from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserCreateWithRole
from app.services.user_service import register_user
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.repositories.user_repo import get_user_by_email
from app.models.user import User, UserRole
from app.core.dependencies import get_db
from app.core.dependencies import require_role

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = register_user(db, user.email, user.password, UserRole.client)
    access_token  = create_access_token({"user_id": db_user.id, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
    #return db_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"user_id": db_user.id, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Registro por admin → puede crear provider o admin
@router.post("/register/admin-create")
def register_by_admin(
    user: UserCreateWithRole,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(UserRole.admin))
):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = register_user(db, user.email, user.password, user.role)
    return {"message": f"User {user.email} created with role {user.role}"}


