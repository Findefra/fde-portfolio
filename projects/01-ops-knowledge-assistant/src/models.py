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
    role: Role = Field(..., description="Caller's role used for permission filtering")
    top_k: Optional[int] = Field(None, ge=1, le=20)


class Source(BaseModel):
    document_id: str
    title: Optional[str] = None
    chunk_id: Optional[str] = None
    score: Optional[float] = None
    excerpt: Optional[str] = None


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


class IngestDocument(BaseModel):
    """Minimal representation of a document ready for ingestion."""

    document_id: str
    title: str
    content: str
    sensitivity: str = "internal"  # e.g. public | internal | restricted
    team: str = "platform"
    version: str = "1.0"
    environment: str = "all"  # e.g. prod | nonprod | all
