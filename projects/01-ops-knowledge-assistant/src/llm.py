"""LLM generation layer.

Starts with a deterministic mock so the API works without external keys.
Swap in Bedrock / OpenAI / Anthropic later behind the same interface.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from models import Source


def generate_answer(
    question: str,
    sources: List[Source],
    *,
    refuse_if_no_sources: bool = True,
    min_best_score: float = 0.25,
) -> Tuple[Optional[str], bool, Optional[str]]:
    """Return (answer, refused, refusal_reason).

    Mock behaviour:
    - If no sources → refuse
    - If best source score is below min_best_score → refuse (weak match)
    - Otherwise → produce a grounded answer that cites the sources
    """
    if not sources and refuse_if_no_sources:
        return (
            None,
            True,
            "Insufficient evidence in the allowed document set for this role.",
        )

    if not sources:
        return (
            "I do not have enough information in the current corpus to answer that.",
            True,
            "No sources retrieved.",
        )

    best = max((s.score or 0.0) for s in sources)
    if best < min_best_score:
        return (
            None,
            True,
            "Retrieved sources are too weakly related to answer confidently.",
        )

    citations = []
    for i, s in enumerate(sources[:3], start=1):
        title = s.title or s.document_id
        sens = f" ({s.sensitivity})" if s.sensitivity else ""
        citations.append(f"[{i}] {title}{sens}")

    answer_parts = [
        f'Based on the available operational documentation, here is a concise answer to: "{question}".',
        "",
        "Key points drawn from the retrieved sources:",
    ]
    for i, s in enumerate(sources[:3], start=1):
        excerpt = (s.excerpt or "").strip()
        if excerpt:
            answer_parts.append(f"- From source [{i}]: {excerpt}")

    answer_parts.append("")
    answer_parts.append("Sources: " + "; ".join(citations))
    answer_parts.append("")
    answer_parts.append(
        "(This is a mock generation response. Replace llm.generate_answer with a real LLM call.)"
    )

    return "\n".join(answer_parts), False, None
