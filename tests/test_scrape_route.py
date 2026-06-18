from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.agents.scraper import ScrapeResult
from app.main import app

client = TestClient(app)


def test_scrape_endpoint_returns_agent_result() -> None:
    mock_result = ScrapeResult(
        url="https://example.com",
        task="Go to https://example.com",
        result="Example Domain",
        steps_taken=2,
    )

    with patch("app.routes.scrape.run_scrape_agent", new=AsyncMock(return_value=mock_result)):
        response = client.post(
            "/api/v1/scrape",
            json={"url": "https://example.com"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://example.com"
    assert data["result"] == "Example Domain"
    assert data["steps_taken"] == 2


def test_scrape_endpoint_rejects_invalid_url() -> None:
    response = client.post("/api/v1/scrape", json={"url": "not-a-url"})
    assert response.status_code == 422


def test_scrape_endpoint_handles_agent_failure() -> None:
    with patch(
        "app.routes.scrape.run_scrape_agent",
        new=AsyncMock(side_effect=RuntimeError("LM Studio unreachable")),
    ):
        response = client.post(
            "/api/v1/scrape",
            json={"url": "https://example.com"},
        )

    assert response.status_code == 502
    assert "LM Studio unreachable" in response.json()["detail"]
