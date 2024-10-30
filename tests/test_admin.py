from fastapi.testclient import TestClient
from fastapi_demo.main import app

client = TestClient(app)

# Mock admin token for testing
admin_token = "test_admin_token"

def test_get_trace_logs():
    response = client.get('/admin/trace-logs', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
