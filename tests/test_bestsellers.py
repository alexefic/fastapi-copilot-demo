from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

def test_get_bestsellers():
    response = client.get("/bestsellers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_bestsellers():
    response = client.get("/bestsellers/search?query=Book")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
