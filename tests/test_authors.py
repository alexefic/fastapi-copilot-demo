from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author, Book
from fastapi import HTTPException

client = TestClient(app)

def test_create_author(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100)
    response = client.post("/books/1/authors", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "other_details": "Test Details"
    })
    assert response.status_code == 201
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("other_details") == "Test Details"
    assert response.json().get("book_id") == 1

def test_create_author_book_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.post("/books/1/authors", json={
        "name": "Test Author",
        "biography": "Test Biography",
        "other_details": "Test Details"
    })
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"

def test_get_author(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Author(id=1, name="Test Author", biography="Test Biography", other_details="Test Details", book_id=1)
    response = client.get("/books/1/authors")
    assert response.status_code == 200
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("other_details") == "Test Details"
    assert response.json().get("book_id") == 1

def test_get_author_not_found(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/books/1/authors")
    assert response.status_code == 404
    assert response.json().get("detail") == "Author not found"