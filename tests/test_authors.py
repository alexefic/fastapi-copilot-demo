from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

def test_create_author(mock_db_session):
    response = client.post("/authors/", json={
        "name": "Author Name",
        "biography": "Bio",
        "other_details": "Details"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Author Name"
    assert response.json()["biography"] == "Bio"
    assert response.json()["other_details"] == "Details"

def test_get_authors(mock_db_session):
    response = client.get("/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
