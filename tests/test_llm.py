from app.config import settings
from app.llm import LMStudioChatOpenAI, build_llm


def test_build_llm_uses_lmstudio_settings() -> None:
    llm = build_llm()
    assert isinstance(llm, LMStudioChatOpenAI)
    assert llm.model == settings.lmstudio_model
    assert str(llm.base_url).rstrip("/") == settings.lmstudio_base_url.rstrip("/")
    assert llm.api_key == settings.lmstudio_api_key
    assert llm.max_completion_tokens == settings.lmstudio_max_completion_tokens
    assert llm.add_schema_to_system_prompt is settings.lmstudio_add_schema_to_system_prompt
    assert llm.dont_force_structured_output is settings.lmstudio_dont_force_structured_output
    assert llm.remove_min_items_from_schema is True
    assert llm.remove_defaults_from_schema is True
    assert llm.timeout is not None
    assert llm.timeout.read == settings.lmstudio_request_timeout
