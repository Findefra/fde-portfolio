# 03 — Architecture & Decisions

## High-Level Design

```
[User / Client]
      |
      | question + role claim
      v
[FastAPI Service]
      |
      +-- Auth / Role extraction
      |
      +-- Permission Filter (metadata)
      |
      +-- Vector Retrieval (pgvector or equivalent)
      |
      +-- Context Assembly + Prompt
      |
      +-- LLM Generation (Bedrock / other)
      |
      +-- Citation + Refusal Logic
      v
[Response: answer + sources  OR  refusal]
```

## Key Components

- **Ingestion**: Offline/batch process that chunks documents, attaches metadata (sensitivity, team, version), generates embeddings, and stores them.
- **Retrieval**: Role is used to construct a metadata filter *before* similarity search. This is intentional — post-generation filtering is weaker for permission safety.
- **Generation**: Prompt requires the model to ground answers in the provided context and to refuse when context is insufficient.
- **Auth**: Portfolio version uses a simple API key + role header. Designed so the role claim can later be replaced by a real IdP group mapping.
- **Storage**: PostgreSQL + pgvector (or managed alternative) for vectors + metadata.
- **Infra**: Terraform-managed AWS resources with least-privilege IAM.

## Architecture Decision Records (to be filled as decisions are made)

### ADR-001: Filter permissions before retrieval
**Status:** Proposed  
**Context:** Need strong guarantee that restricted documents never reach the generation step for unauthorized users.  
**Decision:** Apply metadata filter on role/sensitivity before vector search.  
**Consequences:** Slightly more complex query construction; much stronger safety property than filtering after generation.

### ADR-002: (placeholder)
Add further ADRs here for chunking strategy, embedding model choice, LLM choice, refusal threshold, etc.

## Non-Goals for Architecture (Pilot)

- Multi-region active-active
- Complex agent orchestration
- Real-time change data capture from source systems

## Open Technical Questions

- Exact vector store choice (self-managed pgvector vs Bedrock Knowledge Base vs OpenSearch)
- Embedding model and dimension
- Refusal confidence threshold logic
- How document versioning will be represented in metadata
