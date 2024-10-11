from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

# Test cases for the /search endpoint

def test_search_items_success():
    response = client.get("/search?isbn=9781234567897")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_items_invalid_isbn():
    response = client.get("/search?isbn=invalidisbn")
    assert response.status_code == 400
    assert response.json().get("detail") == "Invalid ISBN format"


def test_search_items_not_found():
    response = client.get("/search?isbn=9780000000000")
    assert response.status_code == 404
    assert response.json().get("detail") == "No items found"


def test_search_items_no_isbn():
    response = client.get("/search")
    assert response.status_code == 422
    assert response.json().get("detail") == "Please enter an ISBN"
