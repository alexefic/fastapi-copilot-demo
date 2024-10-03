from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

def test_search_books_valid_isbn():
    response = client.get("/books/search?isbn=valid_isbn")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Example Book",
        "author": "John Doe",
        "pages": 300,
        "isbn": "valid_isbn"
    }

def test_search_books_invalid_isbn():
    response = client.get("/books/search?isbn=invalid_isbn")
    assert response.status_code == 404
    assert response.json() == {"detail": "No results found"}

def test_search_books_empty_isbn():
    response = client.get("/books/search?isbn=")
    assert response.status_code == 400
    assert response.json() == {"detail": "Please enter an ISBN"}