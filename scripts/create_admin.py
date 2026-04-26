from app.db.session import SessionLocal
from app.services.user_service import register_user
from app.models.user import UserRole

# Script de uso único para crear el primer admin en un entorno nuevo.
# Ejecutar con: docker exec -it gestionturnos-api-1 python -m scripts.create_admin

def create_admin():
    db = SessionLocal()
    try:
        register_user(db, "admin@admin.com", "admin123", UserRole.admin)
        print("Admin created successfully")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()