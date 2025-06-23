import pytest
from fastapi.testclient import TestClient

def test_get_questions(client: TestClient):
    """Test getting all questions."""
    response = client.get("/api/v1/questions")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

# Additional question tests will be implemented here 