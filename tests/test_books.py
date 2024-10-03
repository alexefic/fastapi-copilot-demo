from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book
from fastapi import HTTPException

client = TestClient(app)

@patch('fastapi_demo.routers.books.get_db')
def test_create_book(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "pages": 100,
        "isbn": "1234567890123"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100
    assert response.json().get("isbn") == "1234567890123"

@patch('fastapi_demo.routers.books.get_db')
def test_read_book_success(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, isbn="1234567890123")
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100
    assert response.json().get("isbn") == "1234567890123"

@patch('fastapi_demo.routers.books.get_db')
def test_read_book_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

@patch('fastapi_demo.routers.books.get_db')
def test_update_book_success(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Old Title", author="Old Author", pages=100, isbn="1234567890123")
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200,
        "isbn": "1234567890123"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "New Title"
    assert response.json().get("author") == "New Author"
    assert response.json().get("pages") == 200
    assert response.json().get("isbn") == "1234567890123"

@patch('fastapi_demo.routers.books.get_db')
def test_update_book_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200,
        "isbn": "1234567890123"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

@patch('fastapi_demo.routers.books.get_db')
def test_delete_book_success(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, isbn="1234567890123")
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Book deleted successfully"

@patch('fastapi_demo.routers.books.get_db')
def test_delete_book_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

@patch('fastapi_demo.routers.books.get_db')
def test_search_books_by_isbn_success(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Book(id=1, title="Test Book", author="Test Author", pages=100, isbn="1234567890123")
    ]
    response = client.get("/books/search?isbn=1234567890123")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("title") == "Test Book"
    assert response.json()[0].get("author") == "Test Author"
    assert response.json()[0].get("pages") == 100
    assert response.json()[0].get("isbn") == "1234567890123"

@patch('fastapi_demo.routers.books.get_db')
def test_search_books_by_isbn_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.all.return_value = []
    response = client.get("/books/search?isbn=1234567890123")
    assert response.status_code == 404
    assert response.json().get("detail") == "No items found"

@patch('fastapi_demo.routers.books.get_db')
def test_search_books_by_isbn_invalid_format(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    response = client.get("/books/search?isbn=invalidisbn")
    assert response.status_code == 400
    assert response.json().get("detail") == "Invalid ISBN format"

@patch('fastapi_demo.routers.books.get_db')
def test_search_books_by_isbn_empty(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    response = client.get("/books/search?isbn=")
    assert response.status_code == 400
    assert response.json().get("detail") == "Please enter an ISBN"
