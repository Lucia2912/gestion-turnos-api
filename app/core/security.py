from passlib.context import CryptContext
import hashlib
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer() 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return pwd_context.hash(hashed)
    #return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    password_bytes = plain_password.encode("utf-8")
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return pwd_context.verify(hashed, hashed_password)

