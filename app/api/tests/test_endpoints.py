import pytest
from fastapi.testclient import TestClient
from app.api.endpoints import router
from app.api.database import get_db, Base, db_engine
from sqlalchemy.orm import sessionmaker

# Setup test database
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base.metadata.create_all(bind=db_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the dependency
router.dependency_overrides[get_db] = override_get_db

client = TestClient(router)

@pytest.fixture(scope="module")
def test_client():
    return client

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_post_data(test_client):
    payload = {
        "server_name": "TestServer",
        "metric_name": "CPU_Usage",
        "value": 75,
        "timestamp": "2023-01-01T00:00:00"
    }
    response = test_client.post("/data", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Data saved successfully"

def test_get_all_data(test_client):
    response = test_client.get("/data")
    assert response.status_code == 200
    assert "data" in response.json()