from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)


def test_create_author(mock_db_session):
    response = client.post("/authors/", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "birth_date": "1970-01-01",
        "death_date": "2020-01-01"
    })
    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("birth_date") == "1970-01-01"
    assert response.json().get("death_date") == "2020-01-01"


def test_create_author_validation_error(mock_db_session):
    response = client.post("/authors/", json={
        "name": "",
        "biography": "",
        "birth_date": ""
    })
    assert response.status_code == 422
