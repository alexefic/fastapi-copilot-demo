from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, CartItem
from fastapi_demo.dtos import AddToCartRequest

client = TestClient(app)

mock_db_session = MagicMock()

mock_user = MagicMock()
mock_user.id = 1

app.dependency_overrides[get_db] = lambda: mock_db_session
app.dependency_overrides[get_current_user] = lambda: mock_user


def test_add_to_cart():
    mock_db_session.query.return_value.filter.return_value.first.side_effect = [
        Book(id=1, title="Test Book", author="Test Author", pages=100, price=10.0),
        None
    ]
    response = client.post('/cart/add', json={"book_id": 1, "quantity": 2})
    assert response.status_code == 200
    assert response.json().get("message") == "Book has been added to your cart"
    assert response.json().get("cart").get("total_price") == 20.0


def test_view_cart():
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        CartItem(book_id=1, quantity=2, price=10.0, book=Book(id=1, title="Test Book", author="Test Author", pages=100, price=10.0))
    ]
    response = client.get('/cart')
    assert response.status_code == 200
    assert response.json().get("cart").get("total_price") == 20.0
