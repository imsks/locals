"""MyNeta resolve route tests."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.unit
def test_myneta_resolve_returns_url(client) -> None:
    mock_result = type(
        "R",
        (),
        {"result": '{"url":"https://www.myneta.info/Bihar2025/candidate.php?candidate_id=9","candidate_id":"9","election_slug":"Bihar2025"}'},
    )()
    with patch(
        "app.routes.myneta.run_scrape_agent",
        new=AsyncMock(return_value=mock_result),
    ):
        resp = client.post(
            "/api/v1/scrape/myneta/resolve",
            json={
                "name": "Test Candidate",
                "state": "Bihar",
                "constituency": "AC",
                "election_slug": "Bihar2025",
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "candidate_id=9" in data["url"]


@pytest.mark.unit
def test_myneta_resolve_404_when_no_url(client) -> None:
    mock_result = type("R", (), {"result": "could not find"})()
    with patch(
        "app.routes.myneta.run_scrape_agent",
        new=AsyncMock(return_value=mock_result),
    ):
        resp = client.post(
            "/api/v1/scrape/myneta/resolve",
            json={
                "name": "Nobody",
                "state": "Bihar",
                "constituency": "AC",
                "election_slug": "Bihar2025",
            },
        )
    assert resp.status_code == 404
