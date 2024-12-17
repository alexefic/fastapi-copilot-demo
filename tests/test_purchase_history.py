from fastapi.testclient import TestClient
from fastapi_demo.main import app
from datetime import datetime, timedelta

client = TestClient(app)

# Mock data for testing
mock_purchase_history = [
    {
        "customer_id": 123,
        "book_id": 456,
        "purchase_date": (datetime.utcnow() - timedelta(days=15)).isoformat(),
        "quantity": 1
    },
    {
        "customer_id": 789,
        "book_id": 101,
        "purchase_date": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "quantity": 2
    }
]

def test_get_last_month_purchase_history():
    response = client.get("/purchase-history/last-month")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    for record in response.json():
        assert "customer_id" in record
        assert "book_id" in record
        assert "purchase_date" in record
        assert "quantity" in record

def test_tag_book_for_sale():
    book_id = 1  # Assuming a book with ID 1 exists in the test database
    response = client.post(f"/books/{book_id}/tag-for-sale")
    assert response.status_code == 200
    assert response.json().get("detail") == "Book tagged for sale"
