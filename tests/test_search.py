from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book
from fastapi import HTTPException

client = TestClient(app)

def test_search_valid_isbn(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Book(id=1, title="Example Book", author="John Doe", pages=300, isbn="1234567890")
    ]
    response = client.get("/search?isbn=1234567890")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Example Book",
            "author": "John Doe",
            "pages": 300,
            "isbn": "1234567890"
        }
    ]

def test_search_invalid_isbn(mock_db_session):
    response = client.get("/search?isbn=invalidisbn")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid ISBN"}

def test_search_empty_isbn(mock_db_session):
    response = client.get("/search?isbn=")
    assert response.status_code == 422
    assert response.json() == {"detail": "Etsi paremmin, torvi"}

def test_search_no_items_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = []
    response = client.get("/search?isbn=1234567890")
    assert response.status_code == 404
    assert response.json() == {"detail": "Eipä löydy"}
