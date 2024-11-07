from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

def test_get_genres_success(mock_db_session):
    mock_db_session.query.return_value.distinct.return_value.all.return_value = [("Fiction",), ("Non-Fiction",)]
    response = client.get("/genres/", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    assert response.json() == ["Fiction", "Non-Fiction"]

def test_get_genres_unauthorized(mock_db_session):
    response = client.get("/genres/")
    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"
