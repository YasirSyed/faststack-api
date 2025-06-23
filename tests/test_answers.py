import pytest
from fastapi.testclient import TestClient

def test_get_answers(client: TestClient):
    """Test getting answers for a question."""
    response = client.get("/api/v1/questions/1/answers")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

# Additional answer tests will be implemented here 