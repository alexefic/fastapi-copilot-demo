from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author
from fastapi import HTTPException

client = TestClient(app)

def test_create_author(mock_db_session):
    response = client.post("/authors/", json={
        "name": "Test Author",
        "bio": "Test Bio"
    })
    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("bio") == "Test Bio"

def test_read_author_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Test Author", bio="Test Bio")
    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.json().get("name") == "Test Author"
    assert response.json().get("bio") == "Test Bio"

def test_read_author_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/authors/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"

def test_update_author_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Old Name", bio="Old Bio")
    response = client.put("/authors/1", json={
        "name": "New Name",
        "bio": "New Bio"
    })
    assert response.status_code == 200
    assert response.json().get("name") == "New Name"
    assert response.json().get("bio") == "New Bio"

def test_update_author_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/authors/1", json={
        "name": "New Name",
        "bio": "New Bio"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"
