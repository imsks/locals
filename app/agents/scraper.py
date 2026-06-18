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


LOCAL_LLM_SYSTEM_HINT = (
    "Respond with raw JSON only — no markdown code fences, no ```json blocks. "
    "Match the provided schema exactly. Do NOT include a thinking field. "
    "The action field must be a JSON array. Keep memory under 200 characters. "
    "Call done immediately once you have the answer."
)


def build_scrape_task(url: str, instructions: str | None = None) -> str:
    if instructions:
        return (
            f"Go to {url}. {instructions} "
            "Read the visible page text only — do not click unless necessary. "
            "When you have the answer, call done with a short plain-text result."
        )
    return (
        f"Go to {url}. "
        "Extract the page title, main headings, and key visible text. "
        "When finished, call done with a concise plain-text summary."
    )


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
        llm_timeout=settings.agent_llm_timeout,
        step_timeout=settings.agent_step_timeout,
        enable_planning=settings.agent_enable_planning,
        flash_mode=settings.agent_flash_mode,
        use_thinking=settings.agent_use_thinking,
        use_judge=settings.agent_use_judge,
        max_actions_per_step=settings.agent_max_actions_per_step,
        max_clickable_elements_length=settings.agent_max_clickable_elements_length,
        extend_system_message=LOCAL_LLM_SYSTEM_HINT,
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
