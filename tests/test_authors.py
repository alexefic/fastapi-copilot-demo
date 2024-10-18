from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author
from datetime import datetime

client = TestClient(app)

mock_db_session = MagicMock()

# Override the get_db dependency
app.dependency_overrides[get_db] = lambda: mock_db_session


def test_create_author():
    response = client.post("/authors/", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "other_details": "Test Details"
    })
    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("other_details") == "Test Details"


def test_get_authors():
    mock_db_session.query.return_value.all.return_value = [
        Author(id=1, name="Test Author", biography="Test Biography", other_details="Test Details", created_at=datetime.utcnow())
    ]
    response = client.get("/authors/")
    assert response.status_code == 200
    authors = response.json()
    assert len(authors) == 1
    assert authors[0].get("name") == "Test Author"
    assert authors[0].get("biography") == "Test Biography"
    assert authors[0].get("other_details") == "Test Details"
