from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book
from fastapi import HTTPException

client = TestClient(app)

@patch('fastapi_demo.routers.books.get_db')
def test_search_books(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Book(id=1, title="Example Book Title", author="Author Name", pages=123),
        Book(id=2, title="Another Example Book Title", author="Another Author", pages=456)
    ]

    response = client.get("/books/search?title=Example")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Example Book Title", "author": "Author Name", "pages": 123},
        {"id": 2, "title": "Another Example Book Title", "author": "Another Author", "pages": 456}
    ]

@patch('fastapi_demo.routers.books.get_db')
def test_search_books_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session

    mock_db_session.query.return_value.filter.return_value.all.return_value = []

    response = client.get("/books/search?title=NonExistentTitle")

    assert response.status_code == 404
    assert response.json() == {"detail": "No books found"}
