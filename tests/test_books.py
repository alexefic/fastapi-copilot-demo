from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, Review
from fastapi import HTTPException
from datetime import datetime

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

def test_view_book_reviews(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Review(id=1, book_id=1, user="John Doe", rating=5, comment="Excellent book!", created_at=datetime.utcnow())
    ]
    response = client.get("/books/1/reviews")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("user") == "John Doe"
    assert response.json()[0].get("rating") == 5
    assert response.json()[0].get("comment") == "Excellent book!"

def test_sort_books_by_reviews(mock_db_session):
    mock_db_session.query.return_value.join.return_value.group_by.return_value.order_by.return_value.all.return_value = [
        (1, "Book Title", "Author Name", 4.5, 100)
    ]
    response = client.get("/books/sort?sort_by=reviews")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("book_id") == 1
    assert response.json()[0].get("title") == "Book Title"
    assert response.json()[0].get("author") == "Author Name"
    assert response.json()[0].get("average_rating") == 4.5
    assert response.json()[0].get("review_count") == 100

def test_add_book_to_basket(mock_db_session):
    response = client.post("/basket", json={
        "book_id": 1
    })
    assert response.status_code == 200
    assert response.json().get("message") == "Book added to basket successfully."