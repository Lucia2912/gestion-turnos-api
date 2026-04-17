from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from app.core.jwt import SECRET_KEY, ALGORITHM
from app.core.security import security
from fastapi.security import HTTPAuthorizationCredentials

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        #token = authorization.split(" ")[1]
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")