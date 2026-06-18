from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    lmstudio_base_url: str = "http://localhost:1234/v1"
    lmstudio_api_key: str = "lm-studio"
    lmstudio_model: str = "google/gemma-4-26b-a4b-qat"
    lmstudio_request_timeout: float = 300.0
    lmstudio_max_completion_tokens: int = 4096
    lmstudio_add_schema_to_system_prompt: bool = True
    lmstudio_dont_force_structured_output: bool = True

    agent_max_steps: int = 15
    agent_use_vision: bool = False
    agent_llm_timeout: int = 300
    agent_step_timeout: int = 300
    agent_enable_planning: bool = False
    agent_flash_mode: bool = True
    agent_use_thinking: bool = False
    agent_use_judge: bool = False
    agent_max_actions_per_step: int = 1
    agent_max_clickable_elements_length: int = 8000
    api_host: str = "0.0.0.0"
    api_port: int = 8080


settings = Settings()
