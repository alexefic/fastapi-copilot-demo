from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book
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

def test_read_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100)
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100

def test_read_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"


def test_update_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Old Title", author="Old Author", pages=100)
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200
    })
    assert response.status_code == 200
    assert response.json().get("title") == "New Title"
    assert response.json().get("author") == "New Author"
    assert response.json().get("pages") == 200

def test_update_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_delete_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100)
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Book deleted successfully"

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"


def test_get_books_sorted_by_sales(mock_db_session):
    mock_db_session.query.return_value.order_by.return_value.all.return_value = [
        Book(id=1, title="Book A", author="Author A", pages=100, sales_volume=50, marked_for_sale=False),
        Book(id=2, title="Book B", author="Author B", pages=150, sales_volume=30, marked_for_sale=False)
    ]
    response = client.get("/books/sales")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 2
    assert books[0]["title"] == "Book A"
    assert books[1]["title"] == "Book B"

def test_mark_books_for_sale(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Book(id=1, title="Book A", author="Author A", pages=100, sales_volume=50, marked_for_sale=False),
        Book(id=2, title="Book B", author="Author B", pages=150, sales_volume=30, marked_for_sale=False)
    ]
    response = client.post("/books/mark-for-sale", json={"book_ids": [1, 2]})
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "Books marked for sale successfully"
    assert result["marked_books"] == [1, 2]
