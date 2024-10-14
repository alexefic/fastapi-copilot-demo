from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, CartItem

client = TestClient(app)


def test_add_to_cart(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, price=10.0)
    response = client.post("/cart/add", json={
        "book_id": 1,
        "quantity": 2
    })
    assert response.status_code == 200
    assert response.json().get("message") == "Book has been added to your cart"
    assert response.json().get("cart")["book_id"] == 1
    assert response.json().get("cart")["quantity"] == 2


def test_view_cart(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        CartItem(id=1, user_id=1, book_id=1, quantity=2)
    ]
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title="Test Book", author="Test Author", pages=100, price=10.0)
    response = client.get("/cart")
    assert response.status_code == 200
    assert len(response.json().get("books")) == 1
    assert response.json().get("books")[0]["book_id"] == 1
    assert response.json().get("books")[0]["title"] == "Test Book"
    assert response.json().get("books")[0]["author"] == "Test Author"
    assert response.json().get("books")[0]["quantity"] == 2
    assert response.json().get("books")[0]["price"] == 20.0
    assert response.json().get("total_price") == 20.0
