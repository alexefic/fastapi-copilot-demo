from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author

client = TestClient(app)

mock_db_session = MagicMock()


def test_create_author():
    response = client.post("/authors/", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "date_of_birth": "2000-01-01"
    })
    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("date_of_birth") == "2000-01-01"


def test_read_author_success():
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Test Author", biography="Test Biography", date_of_birth="2000-01-01")
    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("date_of_birth") == "2000-01-01"


def test_read_author_not_found():
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/authors/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"
