from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, Author
from fastapi import HTTPException
from datetime import date

client = TestClient(app)

def test_create_book(mock_db_session):
    response = client.post("/books/", json={
        "title": "Test Book"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"

def test_read_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author_id=1)
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"

def test_read_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_create_author_for_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book")
    response = client.post("/books/1/author", json={
        "name": "John Doe",
        "biography": "An accomplished author",
        "birthdate": "1970-01-01"
    })
    assert response.status_code == 201
    assert response.json().get("author").get("name") == "John Doe"

def test_create_author_for_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.post("/books/1/author", json={
        "name": "John Doe",
        "biography": "An accomplished author",
        "birthdate": "1970-01-01"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_update_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Old Title")
    response = client.put("/books/1", json={
        "title": "New Title"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "New Title"

def test_update_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/books/1", json={
        "title": "New Title"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_delete_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book")
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Book deleted successfully"

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"
