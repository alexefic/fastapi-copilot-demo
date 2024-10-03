from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book
from fastapi import HTTPException

client = TestClient(app)

# Existing tests...

def test_search_books_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Book(id=1, title="Example Book Title", author="Author Name", pages=300, isbn="1234567890")
    ]
    response = client.get("/books/search?isbn=1234567890")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("title") == "Example Book Title"
    assert response.json()[0].get("author") == "Author Name"
    assert response.json()[0].get("pages") == 300

def test_search_books_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = []
    response = client.get("/books/search?isbn=0000000000")
    assert response.status_code == 404
    assert response.json().get("detail") == "No items found for the given ISBN"