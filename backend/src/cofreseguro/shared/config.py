"""Application settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CofreSeguro"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./cofreseguro.db",
        alias="DATABASE_URL",
    )
    jwt_secret: str = Field(
        default="change-me-in-production-use-long-random-string",
        alias="JWT_SECRET",
    )
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 120
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    ollama_enabled: bool = Field(default=False, alias="OLLAMA_ENABLED")
    ollama_timeout_s: float = 8.0
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


@lru_cache
def get_settings() -> Settings:
    return Settings()
