from fastapi.testclient import TestClient
from fastapi_app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/wordle-solver/api/ping")
    assert response.status_code == 200
