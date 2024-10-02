from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Author

client = TestClient(app)

def test_create_author():
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

def test_read_author():
    response = client.get("/books/1/authors")
    assert response.status_code == 200
    assert response.json().get("name") == "Test Author"
    assert response.json().get("biography") == "Test Biography"
    assert response.json().get("other_details") == "Test Details"
    assert response.json().get("book_id") == 1
