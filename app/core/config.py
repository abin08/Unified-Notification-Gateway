from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Unified Notification Gateway"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    API_SECURITY_KEY: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Slack Settings
    # We might not need global slack settings if we pass webhook_url in the payload,
    # but it's good to have a default fallback or for admin alerts.
    DEFAULT_SLACK_WEBHOOK: Optional[str] = None

    # Pydantic Configuration
    # This tells Pydantic to read from a local .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Singleton Pattern for Settings
# using lru_cache ensures we instantiate the Settings object only once
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()