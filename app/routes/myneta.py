"""MyNeta URL resolution via browser-use agent."""

from __future__ import annotations

import json
import re

from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from app.agents.scraper import run_scrape_agent

router = APIRouter()


class MyNetaResolveRequest(BaseModel):
    name: str
    state: str
    constituency: str
    election_slug: str
    max_steps: int | None = 15


class MyNetaResolveResponse(BaseModel):
    url: str | None = None
    candidate_id: str | None = None
    election_slug: str | None = None
    raw_result: str | None = None


def _build_search_url(election_slug: str) -> str:
    slug = election_slug.strip("/")
    return f"https://www.myneta.info/{slug}/"


def _build_instructions(body: MyNetaResolveRequest) -> str:
    return (
        f"Search MyNeta for candidate '{body.name}' from constituency "
        f"'{body.constituency}' in state '{body.state}' for election '{body.election_slug}'. "
        "Navigate to their candidate.php profile page. "
        "When found, call done with raw JSON only (no markdown): "
        '{"url":"https://www.myneta.info/.../candidate.php?candidate_id=NNN",'
        f'"candidate_id":"NNN","election_slug":"{body.election_slug}"}}'
    )


def _parse_result(text: str, election_slug: str) -> MyNetaResolveResponse:
    text = (text or "").strip()
    if not text:
        return MyNetaResolveResponse(raw_result=text)

    try:
        data = json.loads(text)
        if isinstance(data, dict) and data.get("url"):
            return MyNetaResolveResponse(
                url=str(data["url"]),
                candidate_id=str(data.get("candidate_id") or ""),
                election_slug=str(data.get("election_slug") or election_slug),
                raw_result=text,
            )
    except json.JSONDecodeError:
        pass

    url_match = re.search(
        r"(https?://[^\s\"']+candidate\.php\?candidate_id=(\d+))",
        text,
        re.I,
    )
    if url_match:
        return MyNetaResolveResponse(
            url=url_match.group(1),
            candidate_id=url_match.group(2),
            election_slug=election_slug,
            raw_result=text,
        )
    return MyNetaResolveResponse(raw_result=text)


@router.post("/myneta/resolve", response_model=MyNetaResolveResponse)
async def resolve_myneta(body: MyNetaResolveRequest) -> MyNetaResolveResponse:
    search_url = _build_search_url(body.election_slug)
    try:
        scrape_result = await run_scrape_agent(
            search_url,
            _build_instructions(body),
            max_steps=body.max_steps,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"MyNeta resolve agent failed: {exc}",
        ) from exc

    parsed = _parse_result(scrape_result.result, body.election_slug)
    if not parsed.url:
        raise HTTPException(
            status_code=404,
            detail=f"Could not resolve MyNeta URL. Agent output: {scrape_result.result[:500]}",
        )
    return parsed
