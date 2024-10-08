from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author
from fastapi import HTTPException

client = TestClient(app)

@patch('fastapi_demo.routers.authors.get_db')
def test_create_author(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session

    response = client.post("/authors/", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "other_details": "Test Details"
    })

    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("other_details") == "Test Details"

@patch('fastapi_demo.routers.authors.get_db')
def test_create_author_validation_error(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session

    response = client.post("/authors/", json={
        "name": "",
        "biography": "",
        "other_details": ""
    })

    assert response.status_code == 400
    assert response.json().get("detail") is not None
