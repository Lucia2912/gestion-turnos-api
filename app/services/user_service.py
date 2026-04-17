from app.repositories.user_repo import get_user_by_email, create_user
from app.core.security import hash_password
from app.models.user import User

def register_user(db, email, password, role):
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("User already exists")
    user= User(email = email, hashed_password = hash_password(password), role = role)
    return create_user(db, user)