"""FastAPI entrypoint for the Ops Knowledge Assistant.

Run locally:
    uvicorn main:app --reload --app-dir .

Or from the src directory:
    uvicorn main:app --reload
"""

from __future__ import annotations

from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from config import Settings, get_settings
from llm import generate_answer
from models import AskRequest, AskResponse, HealthResponse, Role
from retrieval import retrieve

app = FastAPI(
    title="Ops Knowledge Assistant",
    description=(
        "Permission-aware operational knowledge assistant (FDE portfolio project). "
        "Filters documents by role before retrieval and returns citations or a clear refusal."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Simple API-key + role auth for the portfolio version
# ---------------------------------------------------------------------------

# Map demo API keys → roles. Replace with real IdP claims later.
KEY_TO_ROLE = {
    "dev-key-admin": Role.ADMIN,
    "dev-key-sre": Role.SRE,
    "dev-key-viewer": Role.VIEWER,
}


def get_current_role(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    settings: Settings = Depends(get_settings),
) -> Role:
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )
    role = KEY_TO_ROLE.get(x_api_key)
    if role is None:
        # Fallback: allow the key if it appears in the configured list and default to viewer
        allowed_keys = {k.strip() for k in settings.api_keys.split(",") if k.strip()}
        if x_api_key not in allowed_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        role = Role.VIEWER
    return role


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.environment,
        app_name=settings.app_name,
    )


@app.post(f"{get_settings().api_prefix}/ask", response_model=AskResponse)
def ask(
    body: AskRequest,
    role_from_key: Role = Depends(get_current_role),
    settings: Settings = Depends(get_settings),
) -> AskResponse:
    """Ask an operational question.

    The role used for permission filtering is taken from the API key.
    The role field in the body is accepted for explicitness / future use but
    the server-side role from the key is authoritative for the skeleton.
    """
    # Prefer the authenticated role; allow body.role only if it matches or for testing.
    effective_role = role_from_key

    top_k = body.top_k or settings.top_k
    sources = retrieve(
        question=body.question,
        role=effective_role,
        top_k=top_k,
        min_score=settings.min_similarity,
    )

    answer, refused, refusal_reason = generate_answer(
        question=body.question,
        sources=sources,
    )

    return AskResponse(
        answer=answer,
        sources=sources,
        refused=refused,
        refusal_reason=refusal_reason,
        role_used=effective_role,
    )


@app.get("/")
def root() -> dict:
    return {
        "service": "ops-knowledge-assistant",
        "docs": "/docs",
        "health": "/health",
        "ask": f"{get_settings().api_prefix}/ask",
    }
