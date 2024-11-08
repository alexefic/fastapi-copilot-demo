from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, Cart

client = TestClient(app)

mock_db_session = MagicMock()

# Mock dependency
app.dependency_overrides[get_db] = lambda: mock_db_session


def test_add_to_cart():
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.post("/cart/add", json={"user_id": 1, "book_id": 1})
    assert response.status_code == 200
    assert response.json().get("message") == "Book added to your cart"


def test_get_cart_info():
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        Cart(user_id=1, book_id=1, quantity=1)
    ]
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, price=10.0)
    response = client.get("/cart/1")
    assert response.status_code == 200
    assert response.json().get("user_id") == 1
    assert len(response.json().get("books")) == 1
    assert response.json().get("total_price") == 10.0
