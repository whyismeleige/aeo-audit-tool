from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app
from tests.fixtures import fake_result

client = TestClient(app)


def test_successful_audit():
    with patch(
        "app.api.routes.audit.orchestrate", AsyncMock(return_value=fake_result)
    ) as mock_orchestrate:
        response = client.post("/api/v1/audit", json={"url": "https://example.com"})

        assert response.status_code == 200

        data = response.json()

        assert data["url"] == "https://example.com"
        assert data["overall_score"] == 80
        assert len(data["pages"]) == 1

        mock_orchestrate.assert_awaited_once()

def test_malformed_seed_url():
    response = client.post("/api/v1/audit", json={"url": "abcd"})
    assert response.status_code == 422
    
def test_health_endpoint():
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["status"] == "ok"