from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author

client = TestClient(app)


def test_create_author(mock_db_session):
    response = client.post("/authors/", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "other_details": "Test Details"
    })
    assert response.status_code == 200
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("other_details") == "Test Details"
    assert response.json().get("message") == "Author information has been successfully saved"


def test_read_authors(mock_db_session):
    mock_db_session.query.return_value.all.return_value = [
        Author(id=1, name="Test Author", biography="Test Biography", other_details="Test Details")
    ]
    response = client.get("/authors/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("name") == "Test Author"
    assert response.json()[0].get("biography") == "Test Biography"
    assert response.json()[0].get("other_details") == "Test Details"


def test_update_author(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(
        id=1, name="Old Name", biography="Old Biography", other_details="Old Details"
    )
    response = client.put("/authors/1", json={
        "name": "New Name",
        "biography": "New Biography",
        "other_details": "New Details"
    })
    assert response.status_code == 200
    assert response.json().get("name") == "New Name"
    assert response.json().get("biography") == "New Biography"
    assert response.json().get("other_details") == "New Details"
    assert response.json().get("message") == "Author information has been successfully updated"


def test_update_author_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/authors/1", json={
        "name": "New Name",
        "biography": "New Biography",
        "other_details": "New Details"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"
