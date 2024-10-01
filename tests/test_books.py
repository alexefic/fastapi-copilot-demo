from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

def test_create_book():
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": {"name": "Test Author", "bio": "Test Bio"},
        "pages": 100
    })
    assert response.status_code == 201
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author")["name"] == "Test Author"
    assert response.json().get("author")["bio"] == "Test Bio"
    assert response.json().get("pages") == 100

def test_read_book_success():
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": {"name": "Test Author", "bio": "Test Bio"},
        "pages": 100
    })
    book_id = response.json().get("id")
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json().get("title") == "Test Book"
    assert response.json().get("author")["name"] == "Test Author"
    assert response.json().get("author")["bio"] == "Test Bio"
    assert response.json().get("pages") == 100

def test_read_book_not_found():
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"
