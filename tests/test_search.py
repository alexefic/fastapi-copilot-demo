from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book
from fastapi import HTTPException

client = TestClient(app)

def test_search_books():
    response = client.get("/search?query=Thrash")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for book in response.json():
        assert "Thrash" in book["title"]


def test_create_spotify_link_success():
    response = client.post("/create-spotify-link", json={"book_id": 1})
    assert response.status_code == 200
    assert "spotify_link" in response.json()


def test_create_spotify_link_book_not_found():
    response = client.post("/create-spotify-link", json={"book_id": 999})
    assert response.status_code == 404
    assert response.json().get("detail") == "Book not found"
