"""Retrieval and permission filtering layer.

Permission filtering happens *before* ranking so restricted content never
enters the candidate set for unauthorized roles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from models import Role, Source


@dataclass
class Chunk:
    document_id: str
    chunk_id: str
    title: str
    content: str
    sensitivity: str
    team: str
    version: str
    environment: str
    embedding: Optional[List[float]] = None


ROLE_SENSITIVITY_MAP = {
    Role.ADMIN: {"public", "internal", "restricted"},
    Role.SRE: {"public", "internal", "restricted"},
    Role.VIEWER: {"public", "internal"},
}


def allowed_sensitivities(role: Role) -> set[str]:
    return ROLE_SENSITIVITY_MAP.get(role, {"public"})


_CHUNKS: List[Chunk] = []


def reset_store() -> None:
    global _CHUNKS
    _CHUNKS = []


def add_chunks(chunks: List[Chunk]) -> int:
    _CHUNKS.extend(chunks)
    return len(chunks)


def get_all_chunks() -> List[Chunk]:
    return list(_CHUNKS)


def simple_keyword_score(query: str, text: str) -> float:
    """Naive keyword overlap for the skeleton (no external embedding API)."""
    q_terms = {t for t in query.lower().split() if len(t) > 2}
    t_terms = set(text.lower().split())
    if not q_terms:
        return 0.0
    overlap = len(q_terms & t_terms)
    return overlap / len(q_terms)


def retrieve(
    question: str,
    role: Role,
    top_k: int = 6,
    min_score: float = 0.1,
) -> List[Source]:
    """Return permission-filtered sources for the question.

    Safety property: filter by sensitivity *before* ranking.
    Restricted chunks are never scored for viewer roles.
    """
    allowed = allowed_sensitivities(role)
    candidates = [c for c in _CHUNKS if c.sensitivity in allowed]

    scored: List[tuple[float, Chunk]] = []
    for chunk in candidates:
        score = simple_keyword_score(question, f"{chunk.title} {chunk.content}")
        if score >= min_score:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    sources: List[Source] = []
    for score, chunk in top:
        sources.append(
            Source(
                document_id=chunk.document_id,
                title=chunk.title,
                chunk_id=chunk.chunk_id,
                score=round(score, 4),
                excerpt=chunk.content[:300] + ("..." if len(chunk.content) > 300 else ""),
                sensitivity=chunk.sensitivity,
            )
        )
    return sources
