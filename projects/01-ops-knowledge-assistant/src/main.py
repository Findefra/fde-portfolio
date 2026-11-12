"""FastAPI entrypoint for the Ops Knowledge Assistant.

Run locally:
    uvicorn main:app --reload

The corpus is loaded into the in-memory store on startup so a separate
ingest process is not required for the local demo (ingest.py still works
for re-ingestion during development).
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from config import Settings, get_settings
from ingest import ingest_corpus
from llm import generate_answer
from models import AskRequest, AskResponse, HealthResponse, Role
from retrieval import get_all_chunks, retrieve


def _default_corpus_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "corpus"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the sample corpus into the in-memory store on startup."""
    settings = get_settings()
    corpus = Path(settings.corpus_path)
    if not corpus.is_absolute():
        corpus = Path(__file__).resolve().parent / corpus
    if not corpus.exists():
        corpus = _default_corpus_path()

    if corpus.exists():
        count = ingest_corpus(corpus)
        print(f"[startup] Loaded {count} chunks from {corpus}")
    else:
        print(f"[startup] WARNING: corpus not found at {corpus} — store is empty")
    yield


app = FastAPI(
    title="Ops Knowledge Assistant",
    description=(
        "Permission-aware operational knowledge assistant (FDE portfolio project). "
        "Filters documents by role *before* retrieval and returns citations or a clear refusal."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


KEY_TO_ROLE = {
    "dev-key-admin": Role.ADMIN,
    "dev-key-sre": Role.SRE,
    "dev-key-viewer": Role.VIEWER,
}


def get_current_role(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    settings: Settings = Depends(get_settings),
) -> Role:
    """Resolve the caller's role from the X-API-Key header.

    The role is authoritative for permission filtering. Body.role is ignored
    for safety so clients cannot escalate by sending a higher role in JSON.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )
    role = KEY_TO_ROLE.get(x_api_key)
    if role is None:
        allowed_keys = {k.strip() for k in settings.api_keys.split(",") if k.strip()}
        if x_api_key not in allowed_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        role = Role.VIEWER
    return role


@app.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.environment,
        app_name=settings.app_name,
        chunks_loaded=len(get_all_chunks()),
    )


@app.post(f"{get_settings().api_prefix}/ask", response_model=AskResponse)
def ask(
    body: AskRequest,
    role_from_key: Role = Depends(get_current_role),
    settings: Settings = Depends(get_settings),
) -> AskResponse:
    """Ask an operational question.

    Permission filtering uses the role derived from the API key only.
    Restricted documents never enter the candidate set for unauthorized roles.
    """
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
