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
        "pages": 100,
        "genre": "romantic-sci-fi"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100
    assert response.json().get("genre") == "romantic-sci-fi"

def test_read_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, genre="romantic-sci-fi")
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100
    assert response.json().get("genre") == "romantic-sci-fi"

def test_read_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_update_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Old Title", author="Old Author", pages=100, genre="romantic-sci-fi")
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200,
        "genre": "romantic-sci-fi"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "New Title"
    assert response.json().get("author") == "New Author"
    assert response.json().get("pages") == 200
    assert response.json().get("genre") == "romantic-sci-fi"

def test_update_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200,
        "genre": "romantic-sci-fi"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_delete_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, genre="romantic-sci-fi")
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Book deleted successfully"

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_search_books(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Book(id=1, title="Romantic Sci-Fi Book 1", author="Author A", pages=300, genre="romantic-sci-fi"),
        Book(id=2, title="Romantic Sci-Fi Book 2", author="Author B", pages=250, genre="romantic-sci-fi")
    ]
    response = client.get("/books/search?genre=romantic-sci-fi")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 2
    assert books[0]["title"] == "Romantic Sci-Fi Book 1"
    assert books[1]["title"] == "Romantic Sci-Fi Book 2"

def test_add_to_cart(mock_db_session):
    response = client.post("/cart", json={
        "book_id": 1,
        "quantity": 1
    })
    assert response.status_code == 201
    assert response.json().get("message") == "Book added to cart"

def test_proceed_to_checkout(mock_db_session):
    response = client.post("/checkout", json={
        "address": "123 Main St, Anytown, USA",
        "delivery_option": "2-day"
    })
    assert response.status_code == 200
    assert response.json().get("payment_link") == "https://paymentgateway.com/checkout/12345"

def test_complete_payment(mock_db_session):
    response = client.post("/payment/complete", json={
        "payment_id": "abc123",
        "status": "success"
    })
    assert response.status_code == 200
    assert response.json().get("order_id") == "12345"
    assert response.json().get("delivery_date") == "2023-10-04"
