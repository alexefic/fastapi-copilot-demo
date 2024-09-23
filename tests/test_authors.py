from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author
from datetime import datetime

client = TestClient(app)

def test_create_author(mock_db_session):
    response = client.post("/authors/", json={
        "name": "Test Author",
        "biography": "Test biography."
    })
    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test biography."

def test_read_author_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(
        id=1, name="Test Author", biography="Test biography.", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
    )
    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test biography."

def test_read_author_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/authors/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"
