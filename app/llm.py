from browser_use import ChatOpenAI

from app.config import settings


def build_llm() -> ChatOpenAI:
    """LM Studio exposes an OpenAI-compatible API at localhost:1234/v1."""
    return ChatOpenAI(
        model=settings.lmstudio_model,
        base_url=settings.lmstudio_base_url,
        api_key=settings.lmstudio_api_key,
        temperature=0.2,
        remove_min_items_from_schema=True,
        remove_defaults_from_schema=True,
    )
