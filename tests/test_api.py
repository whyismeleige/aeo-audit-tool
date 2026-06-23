from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app
from app.api.dependencies import rate_limit_check
from tests.fixtures import fake_job_id, fake_successful_job_response

client = TestClient(app)

app.dependency_overrides[rate_limit_check] = lambda: None


@patch("app.api.routes.audit.create_job", new_callable=AsyncMock)
@patch("app.api.routes.audit.run_audit_task")
def test_successful_job_creation(mock_run_audit_task, mock_create_job):
    mock_create_job.return_value = fake_job_id

    response = client.post(
        "/api/v1/audit",
        json={"url": "https://example.com", "email": "sample@example.com"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == fake_job_id

    mock_create_job.assert_awaited_once()
    mock_run_audit_task.delay.assert_called_once()


def test_malformed_seed_url():
    response = client.post(
        "/api/v1/audit", json={"url": "abcd", "email": "sample@example.com"}
    )
    assert response.status_code == 422


def test_invalid_email():
    response = client.post(
        "/api/v1/audit", json={"url": "https://example.com", "email": "invalid-email"}
    )
    assert response.status_code == 422


@patch("app.api.routes.audit.create_job", new_callable=AsyncMock)
@patch("app.api.routes.audit.run_audit_task")
def test_run_audit_server_error(_, mock_create_job):
    mock_create_job.side_effect = Exception("DB Error")

    response = client.post(
        "/api/v1/audit",
        json={"url": "https://example.com", "email": "sample@example.com"},
    )

    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == "An unexpected error occured during the audit. Please try again."
    )

    mock_create_job.assert_awaited_once()


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


@patch("app.api.routes.audit.get_job", new_callable=AsyncMock)
def test_job_found(mock_get_job):
    mock_get_job.return_value = fake_successful_job_response

    response = client.get(f"/api/v1/audit/{fake_job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["job_id"] == fake_job_id

    mock_get_job.assert_awaited_once()


@patch("app.api.routes.audit.get_job", new_callable=AsyncMock)
def test_job_not_found(mock_get_job):
    mock_get_job.return_value = None

    response = client.get(f"/api/v1/audit/{fake_job_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Audit job was not found."

    mock_get_job.assert_awaited_once()


@patch("app.api.routes.audit.get_job", new_callable=AsyncMock)
def test_get_audit_server_error(mock_get_job):
    mock_get_job.side_effect = Exception("DB Error")

    response = client.get(f"/api/v1/audit/{fake_job_id}")

    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == "An unexpected error occured during the audit. Please try again."
    )

    mock_get_job.assert_awaited_once()
