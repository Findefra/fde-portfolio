"""Application configuration."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ops-knowledge-assistant"
    environment: Literal["local", "dev", "staging", "prod"] = "local"
    debug: bool = True

    api_prefix: str = "/api/v1"
    api_keys: str = "dev-key-admin,dev-key-sre,dev-key-viewer"

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/ops_kb"
    embedding_dimension: int = 1536

    llm_provider: Literal["mock", "bedrock", "openai", "anthropic"] = "mock"
    embedding_provider: Literal["mock", "bedrock", "openai"] = "mock"

    top_k: int = 6
    min_similarity: float = 0.15

    corpus_path: str = "../data/corpus"


@lru_cache
def get_settings() -> Settings:
    return Settings()
