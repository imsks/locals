from pydantic import BaseModel, HttpUrl

from fastapi import APIRouter, HTTPException

from app.agents.scraper import run_scrape_agent

router = APIRouter()


class ScrapeRequest(BaseModel):
    url: HttpUrl
    instructions: str | None = None
    max_steps: int | None = None


class ScrapeResponse(BaseModel):
    url: str
    task: str
    result: str
    steps_taken: int


@router.post("", response_model=ScrapeResponse)
async def scrape_website(body: ScrapeRequest) -> ScrapeResponse:
    url = str(body.url)
    try:
        scrape_result = await run_scrape_agent(
            url,
            body.instructions,
            max_steps=body.max_steps,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Scrape agent failed: {exc}") from exc

    return ScrapeResponse(
        url=scrape_result.url,
        task=scrape_result.task,
        result=scrape_result.result,
        steps_taken=scrape_result.steps_taken,
    )
