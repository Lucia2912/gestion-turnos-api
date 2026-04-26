from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from app.core.jwt import SECRET_KEY, ALGORITHM
from app.core.security import security
from fastapi.security import HTTPAuthorizationCredentials
from app.db.session import SessionLocal
from app.models.user import UserRole

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "role": role} 
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(*roles: UserRole):
    def checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return current_user
    return checker