from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.scraper import ScrapeResult, build_scrape_task, run_scrape_agent


def test_build_scrape_task_includes_url() -> None:
    task = build_scrape_task("https://example.com")
    assert "https://example.com" in task
    assert "Extract" in task


def test_build_scrape_task_with_instructions() -> None:
    task = build_scrape_task("https://example.com", "Get all product prices")
    assert "Get all product prices" in task


@pytest.mark.asyncio
async def test_run_scrape_agent_returns_result() -> None:
    mock_history = MagicMock()
    mock_history.final_result.return_value = "Page title: Example"
    mock_history.__len__.return_value = 3

    mock_agent_instance = MagicMock()
    mock_agent_instance.run = AsyncMock(return_value=mock_history)

    with patch("app.agents.scraper.Agent", return_value=mock_agent_instance):
        result = await run_scrape_agent("https://example.com")

    assert isinstance(result, ScrapeResult)
    assert result.url == "https://example.com"
    assert result.result == "Page title: Example"
    assert result.steps_taken == 3
    mock_agent_instance.run.assert_awaited_once()
