"""Application configuration.

Uses pydantic-settings so values can come from environment variables or a .env file.
Keep secrets out of source control.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "ops-knowledge-assistant"
    environment: Literal["local", "dev", "staging", "prod"] = "local"
    debug: bool = True

    # API
    api_prefix: str = "/api/v1"
    # Simple API-key auth for the portfolio version.
    # In a real engagement this would map to an IdP role claim.
    api_keys: str = "dev-key-admin,dev-key-sre,dev-key-viewer"  # comma-separated

    # Database / vector store
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/ops_kb"
    embedding_dimension: int = 1536  # adjust to your embedding model

    # LLM / embeddings (placeholders — wire to Bedrock or OpenAI later)
    llm_provider: Literal["mock", "bedrock", "openai", "anthropic"] = "mock"
    embedding_provider: Literal["mock", "bedrock", "openai"] = "mock"

    # Retrieval defaults
    top_k: int = 6
    min_similarity: float = 0.25  # tune later against eval set

    # Corpus location used by the ingestion script
    corpus_path: str = "../data/corpus"


@lru_cache
def get_settings() -> Settings:
    return Settings()
