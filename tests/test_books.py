from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book
from fastapi import HTTPException

client = TestClient(app)

def test_create_book(mock_db_session):
    response = client.post("/books/", json={
        "title": "Test Book",
        "authors": ["Test Author 1", "Test Author 2"],
        "pages": 100
    })
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("authors") == ["Test Author 1", "Test Author 2"]
    assert response.json().get("pages") == 100

def test_read_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", authors="Test Author 1,Test Author 2", pages=100)
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("authors") == ["Test Author 1", "Test Author 2"]
    assert response.json().get("pages") == 100

def test_read_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_update_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Old Title", authors="Old Author", pages=100)
    response = client.put("/books/1", json={
        "title": "New Title",
        "authors": ["New Author 1", "New Author 2"],
        "pages": 200
    })
    assert response.status_code == 200
    assert response.json().get("title") == "New Title"
    assert response.json().get("authors") == ["New Author 1", "New Author 2"]
    assert response.json().get("pages") == 200

def test_update_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/books/1", json={
        "title": "New Title",
        "authors": ["New Author 1", "New Author 2"],
        "pages": 200
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_delete_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", authors="Test Author 1,Test Author 2", pages=100)
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Book deleted successfully"

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_delete_books_with_multiple_authors(mock_db_session):
    book1 = Book(id=1, title="Book 1", authors="Author 1,Author 2,Author 3", pages=100)
    book2 = Book(id=2, title="Book 2", authors="Author 1,Author 2", pages=150)
    mock_db_session.query.return_value.filter.return_value.all.return_value = [book1]
    response = client.post("/books/delete-multiple-authors", headers={"Authorization": "Bearer admin_token"})
    assert response.status_code == 200
    assert len(response.json()["deleted_books"]) == 1
    assert response.json()["deleted_books"][0]["title"] == "Book 1"
