"""Application settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, model_validator
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
    refresh_expire_days: int = 14
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    ollama_enabled: bool = Field(default=False, alias="OLLAMA_ENABLED")
    ollama_timeout_s: float = 8.0
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    fusion_weight_rules: float = Field(default=0.45, alias="FUSION_WEIGHT_RULES")
    fusion_weight_ml: float = Field(default=0.35, alias="FUSION_WEIGHT_ML")
    fusion_weight_url: float = Field(default=0.35, alias="FUSION_WEIGHT_URL")
    rate_limit_analyze: int = Field(default=120, alias="RATE_LIMIT_ANALYZE")
    rate_limit_auth: int = Field(default=30, alias="RATE_LIMIT_AUTH")
    max_failed_logins: int = 5
    lockout_minutes: int = 15

    @model_validator(mode="after")
    def _prod_secret_guard(self) -> Settings:
        if self.environment == "production" and self.jwt_secret.startswith("change-me"):
            raise ValueError("JWT_SECRET must be set in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
