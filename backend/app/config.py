"""Central settings — reads from env vars / .env file.

Single source of truth for URLs, credentials, and tunables. Modules should
`from app.config import settings` rather than reading os.environ directly.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings. Env vars > .env file > class defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------ meta
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", alias="BACKEND_LOG_LEVEL"
    )

    cors_origins: str = Field(
        default="http://localhost:3000", alias="BACKEND_CORS_ORIGINS"
    )

    # ------------------------------------------------------------ PostgreSQL
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_user: str = Field(default="raglens", alias="POSTGRES_USER")
    postgres_password: str = Field(default="raglens", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="raglens", alias="POSTGRES_DB")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """Async SQLAlchemy URL using psycopg v3 driver."""
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ------------------------------------------------------------- ClickHouse
    clickhouse_host: str = Field(default="localhost", alias="CLICKHOUSE_HOST")
    clickhouse_http_port: int = Field(default=8123, alias="CLICKHOUSE_HTTP_PORT")
    clickhouse_native_port: int = Field(default=9000, alias="CLICKHOUSE_NATIVE_PORT")
    clickhouse_user: str = Field(default="raglens", alias="CLICKHOUSE_USER")
    clickhouse_password: str = Field(default="raglens", alias="CLICKHOUSE_PASSWORD")
    clickhouse_database: str = Field(default="raglens", alias="CLICKHOUSE_DATABASE")

    # ------------------------------------------------------------------ Redis
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_stream_ingest: str = Field(default="raglens:ingest", alias="REDIS_STREAM_INGEST")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # ----------------------------------------------------------------- Qdrant
    qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
    qdrant_http_port: int = Field(default=6333, alias="QDRANT_HTTP_PORT")

    # ------------------------------------------------------------ Ingest tune
    ingest_batch_size: int = Field(default=100, alias="INGEST_BATCH_SIZE")
    ingest_batch_timeout_ms: int = Field(default=1000, alias="INGEST_BATCH_TIMEOUT_MS")

    # -------------------------------------------------------- LLM (eval judge)
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    deepseek_api_key: str | None = Field(default=None, alias="DEEPSEEK_API_KEY")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings instance. Tests can `get_settings.cache_clear()` to reload."""
    return Settings()


# Module-level shortcut for the 95% of code that just wants `settings.foo`.
settings = get_settings()
