from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author

client = TestClient(app)


def test_create_author(mock_db_session):
    response = client.post("/authors/", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "date_of_birth": "2000-01-01"
    })
    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("date_of_birth") == "2000-01-01"


def test_update_author_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Old Name", biography="Old Biography", date_of_birth="2000-01-01")
    response = client.put("/authors/1", json={
        "name": "New Name",
        "biography": "New Biography",
        "date_of_birth": "1990-01-01"
    })
    assert response.status_code == 200
    assert response.json().get("name") == "New Name"
    assert response.json().get("biography") == "New Biography"
    assert response.json().get("date_of_birth") == "1990-01-01"


def test_update_author_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/authors/1", json={
        "name": "New Name",
        "biography": "New Biography",
        "date_of_birth": "1990-01-01"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"


def test_get_author_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Test Author", biography="Test Biography", date_of_birth="2000-01-01")
    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("date_of_birth") == "2000-01-01"


def test_get_author_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/authors/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"
