"""Pydantic models for API requests and responses."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Role(str, Enum):
    """Simple role model for the portfolio version.

    In a real engagement these would map to IdP groups.
    """

    ADMIN = "admin"
    SRE = "sre"
    VIEWER = "viewer"


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)
    role: Optional[Role] = Field(
        None,
        description=(
            "Optional client-declared role for documentation only. "
            "The server always uses the role bound to the API key."
        ),
    )
    top_k: Optional[int] = Field(None, ge=1, le=20)


class Source(BaseModel):
    document_id: str
    title: Optional[str] = None
    chunk_id: Optional[str] = None
    score: Optional[float] = None
    excerpt: Optional[str] = None
    sensitivity: Optional[str] = Field(
        None,
        description="Document sensitivity label (public | internal | restricted)",
    )


class AskResponse(BaseModel):
    answer: Optional[str] = None
    sources: List[Source] = Field(default_factory=list)
    refused: bool = False
    refusal_reason: Optional[str] = None
    role_used: Role


class HealthResponse(BaseModel):
    status: str = "ok"
    environment: str
    app_name: str
    chunks_loaded: int = 0


class IngestDocument(BaseModel):
    """Minimal representation of a document ready for ingestion."""

    document_id: str
    title: str
    content: str
    sensitivity: str = "internal"
    team: str = "platform"
    version: str = "1.0"
    environment: str = "all"
