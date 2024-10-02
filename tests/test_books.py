from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, Author
from fastapi import HTTPException

client = TestClient(app)

def test_create_book(mock_db_session):
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": {"name": "Test Author", "bio": "Test Bio"},
        "pages": 100
    })
    assert response.status_code == 201
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author").get("name") == "Test Author"
    assert response.json().get("author").get("bio") == "Test Bio"
    assert response.json().get("pages") == 100

def test_read_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author_id=1, pages=100)
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Test Author", bio="Test Bio")
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author").get("name") == "Test Author"
    assert response.json().get("author").get("bio") == "Test Bio"
    assert response.json().get("pages") == 100

def test_read_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_update_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Old Title", author_id=1, pages=100)
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Old Author", bio="Old Bio")
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": {"name": "New Author", "bio": "New Bio"},
        "pages": 200
    })
    assert response.status_code == 200
    assert response.json().get("title") == "New Title"
    assert response.json().get("author").get("name") == "New Author"
    assert response.json().get("author").get("bio") == "New Bio"
    assert response.json().get("pages") == 200

def test_update_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": {"name": "New Author", "bio": "New Bio"},
        "pages": 200
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_delete_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author_id=1, pages=100)
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Book deleted successfully"

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"
