import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
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

# Create a FastAPI app instance
app = FastAPI()
app.include_router(router)

# Override the dependency on the app instance
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_post_data(test_client):
    payload = [
        {
            "server_name": "TestServer",
            "metric_name": "CPU_Usage",
            "value": 75,
            "timestamp": "2023-01-01T00:00:00"
        }
    ]
    response = test_client.post("/data", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Data saved successfully"

def test_get_all_data(test_client):
    response = test_client.get("/data")
    assert response.status_code == 200
    assert "data" in response.json()

@pytest.mark.parametrize("payload", [
    [{"server_name": "TestServer1", "metric_name": "Memory_Usage", "value": 60, "timestamp": "2023-01-01T01:00:00"}],
    [{"server_name": "TestServer2", "metric_name": "Disk_Usage", "value": 80, "timestamp": "2023-01-01T02:00:00"}]
])
def test_post_multiple_data(test_client, payload):
    response = test_client.post("/data", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Data saved successfully"

def test_get_data_by_id(test_client):
    # Assuming an item with ID 1 exists
    response = test_client.get("/data/1")
    assert response.status_code == 200
    assert "server_name" in response.json()
    assert "metric_name" in response.json()
    assert "value" in response.json()
    assert "timestamp" in response.json()