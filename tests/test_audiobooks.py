from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

def test_download_audiobook():
    response = client.post("/audiobooks/1/download")
    assert response.status_code == 200
    assert response.json().get("download_url") == "https://example.com/audiobooks/1/download"
    assert response.json().get("progress") == 0


def test_get_download_progress():
    response = client.get("/audiobooks/1/download/progress")
    assert response.status_code == 200
    assert response.json().get("audiobook_id") == 1
    assert response.json().get("progress") == 0
