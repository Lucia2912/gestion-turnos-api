import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import SessionLocal
from app.core.dependencies import get_db

# BD en memoria solo para tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobreescribir get_db para usar la BD de tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # Crea las tablas antes de cada test y las borra después
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def registered_client(client):
    client.post("/auth/register", json={
        "email": "client@test.com",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "client@test.com",
        "password": "password123"
    })
    token = response.json()["access_token"]
    return {"client": client, "token": token}