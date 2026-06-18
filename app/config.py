from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    lmstudio_base_url: str = "http://localhost:1234/v1"
    lmstudio_api_key: str = "lm-studio"
    lmstudio_model: str = "google/gemma-4-26b-a4b-qat"
    agent_max_steps: int = 15
    agent_use_vision: bool = False
    api_host: str = "0.0.0.0"
    api_port: int = 8080


settings = Settings()
