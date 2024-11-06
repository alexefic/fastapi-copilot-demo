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
        "hci_number": "HCI12345",
        "genre": "fantasy"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100
    assert response.json().get("hci_number") == "HCI12345"
    assert response.json().get("genre") == "fantasy"


def test_read_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, hci_number="HCI12345", genre="fantasy")
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author") == "Test Author"
    assert response.json().get("pages") == 100
    assert response.json().get("hci_number") == "HCI12345"
    assert response.json().get("genre") == "fantasy"


def test_read_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"


def test_update_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Old Title", author="Old Author", pages=100, hci_number="HCI12345", genre="fantasy")
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200,
        "hci_number": "HCI67890",
        "genre": "fantasy"
    })
    assert response.status_code == 200
    assert response.json().get("title") == "New Title"
    assert response.json().get("author") == "New Author"
    assert response.json().get("pages") == 200
    assert response.json().get("hci_number") == "HCI67890"
    assert response.json().get("genre") == "fantasy"


def test_update_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put("/books/1", json={
        "title": "New Title",
        "author": "New Author",
        "pages": 200,
        "hci_number": "HCI67890",
        "genre": "fantasy"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"


def test_delete_book_success(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, hci_number="HCI12345", genre="fantasy")
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Book deleted successfully"


def test_delete_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"


def test_get_fantasy_books_hci(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Book(id=1, title="Fantasy Book 1", author="Author 1", pages=300, hci_number="HCI12345", genre="fantasy"),
        Book(id=2, title="Fantasy Book 2", author="Author 2", pages=350, hci_number="HCI67890", genre="fantasy"),
        Book(id=3, title="Fantasy Book 3", author="Author 3", pages=400, hci_number="HCI54321", genre="fantasy")
    ]
    response = client.get("/books/fantasy/hci")
    assert response.status_code == 200
    assert response.json() == {
        "hci_numbers": [
            "HCI12345",
            "HCI67890",
            "HCI54321"
        ]
    }
