from app.config import settings
from app.llm import build_llm


def test_build_llm_uses_lmstudio_settings() -> None:
    llm = build_llm()
    assert llm.model == settings.lmstudio_model
    assert str(llm.base_url).rstrip("/") == settings.lmstudio_base_url.rstrip("/")
    assert llm.api_key == settings.lmstudio_api_key
    assert llm.remove_min_items_from_schema is True
    assert llm.remove_defaults_from_schema is True
