from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "supersecretkey" #luego va en .env
ALGORITHM = "HS256"

def create_access_token(data: dict, expire_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
