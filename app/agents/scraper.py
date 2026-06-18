from dataclasses import dataclass

from browser_use import Agent

from app.config import settings
from app.llm import build_llm


@dataclass
class ScrapeResult:
    url: str
    task: str
    result: str
    steps_taken: int


def build_scrape_task(url: str, instructions: str | None = None) -> str:
    base = (
        f"Go to {url}. "
        "Extract the page's main content: title, headings, paragraphs, links, and any visible structured data. "
        "Return a concise structured summary as plain text."
    )
    if instructions:
        return f"{base} Additional instructions: {instructions}"
    return base


async def run_scrape_agent(
    url: str,
    instructions: str | None = None,
    *,
    max_steps: int | None = None,
) -> ScrapeResult:
    task = build_scrape_task(url, instructions)
    llm = build_llm()

    agent = Agent(
        task=task,
        llm=llm,
        use_vision=settings.agent_use_vision,
    )

    history = await agent.run(max_steps=max_steps or settings.agent_max_steps)
    final = history.final_result() or ""
    steps_taken = len(history)

    return ScrapeResult(
        url=url,
        task=task,
        result=final or "",
        steps_taken=steps_taken,
    )
