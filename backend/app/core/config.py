"""Application configuration.

Single source of truth for settings (SRP). Values come from environment / .env,
validated by Pydantic. Nothing else in the app reads os.environ directly.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="COUNTR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Product identity (branding is centralized here — see ADR-0007).
    app_name: str = "Countr"
    app_vendor: str = "BallotDA"

    env: str = "local"
    debug: bool = True

    database_url: str = "postgresql+psycopg://countr:countr@localhost:5432/countr"

    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000"

    # Auth / JWT. Override secret in every non-local environment.
    jwt_secret: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 60 * 12

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached accessor so settings are parsed once (used via DI)."""
    return Settings()
