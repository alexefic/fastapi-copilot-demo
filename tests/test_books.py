# FILEPATH: /Users/alexjantunen/dev/fast-api-demo/test_main.py
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app, get_db, Book, BookUpdate
from fastapi import HTTPException

client = TestClient(app)

def test_create_book(mock_db_session):
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "pages": 100
    })

    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100

def test_read_book(mock_db_session):

    # Mock the Book model
    mock_book = MagicMock(spec=Book)
    mock_book.id = 1
    mock_book.title = "Test Book"
    mock_book.author = "Test Author"
    mock_book.pages = 100

    # Mock the query filter and first methods
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_book

    response = client.get("/books/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Book",
        "author": "Test Author",
        "pages": 100
    }

def test_read_book_not_found(mock_db_session):
    # Mock the query filter and first methods
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    response = client.get("/books/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_update_book(mock_db_session):
    
    # Mock the Book Model
    mock_book = MagicMock(spec=Book)
    mock_book.id = 1
    mock_book.title = "Test Book"
    mock_book.author = "Test Author"
    mock_book.pages = 100

    # Create a BookUpdate instance
    book_update = BookUpdate(
        title="Updated Test Book",
        author="Updated Test Author",
        pages=200
    )

    # Mock the query filter and first methods
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_book

    response = client.put("/books/1", json=book_update.model_dump())

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "pages": 200
    }

def test_update_book_fails_because_not_found(mock_db_session):
    # Mock the query filter and first methods
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    response = client.put("/books/1", json={
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "pages": 200
    })

    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_delete_book(mock_db_session):
    # Mock the Book model
    mock_book = MagicMock(spec=Book)
    mock_book.id = 1
    mock_book.title = "Test Book"
    mock_book.author = "Test Author"
    mock_book.pages = 100

    # Mock the query filter and first methods
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_book

    response = client.delete("/books/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "Book deleted"}

def test_delete_book_not_found(mock_db_session):
    
    # Mock the query filter and first methods
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    response = client.delete("/books/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}