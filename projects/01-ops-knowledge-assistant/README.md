# 01 — Ops Knowledge Assistant

**Status:** In Progress  
**Type:** Permission-aware RAG over operational documentation

## Customer Problem (Fictional Engagement)

A mid-size cloud operations team maintains runbooks, CIS hardening guides, Terraform module documentation, architecture notes, and incident post-mortems across Confluence, S3, and Git. Engineers spend significant time hunting for answers and occasionally act on outdated or restricted guidance.

They want a single assistant that:
- Answers operational questions with precise source citations
- Respects role-based access (certain production runbooks are restricted)
- Clearly refuses when evidence is insufficient or the user lacks permission
- Can be operated and monitored by the existing platform team

## Success Criteria (Pilot)
- Correctly answers a defined set of operational questions with accurate citations
- Never surfaces restricted content to unauthorized roles
- Returns a clear "I don't know / insufficient evidence" response when appropriate
- Deployed on AWS with basic observability and least-privilege IAM
- Includes evaluation results and a usable runbook

## Repository Layout

```
01-ops-knowledge-assistant/
├─ README.md
├─ docs/
│   ├─ 01-discovery.md
│   ├─ 02-scope.md
│   ├─ 03-architecture.md
│   ├─ 04-evaluation.md
│   ├─ 05-runbook.md
│   └─ 06-handoff.md
├─ src/                 # FastAPI app, ingestion, retrieval, mock LLM
├─ data/corpus/         # Sample documents (public / internal / restricted)
├─ terraform/           # Infrastructure (to be added)
└─ evals/               # Evaluation questions and results
```

## Current Progress

- [x] Repository and documentation skeleton created
- [x] FastAPI + ingestion + retrieval skeleton (in-memory, mock LLM)
- [x] Sample corpus with public / internal / restricted documents
- [ ] Discovery and scope documents refined as needed
- [ ] Real embeddings + vector store (pgvector / Bedrock)
- [ ] Evaluation set and baseline metrics
- [ ] AWS deployment via Terraform
- [ ] Runbook and handoff complete

## How to Run the Skeleton

### 1. Setup

```bash
cd projects/01-ops-knowledge-assistant/src
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # optional
```

### 2. Ingest the sample corpus

```bash
python ingest.py --corpus ../data/corpus
```

You should see the three sample documents being loaded with their sensitivity labels.

### 3. Start the API

```bash
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000/docs for the interactive Swagger UI.

### 4. Example requests

**Health**
```bash
curl http://localhost:8000/health
```

**Ask as SRE (can see restricted)**
```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-sre" \
  -d '{"question": "What is the production break-glass procedure?", "role": "sre"}'
```

**Ask as Viewer (should refuse restricted content)**
```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-viewer" \
  -d '{"question": "What is the production break-glass procedure?", "role": "viewer"}'
```

**Demo API keys**
| Key | Role |
|-----|------|
| `dev-key-admin` | admin |
| `dev-key-sre` | sre |
| `dev-key-viewer` | viewer |

## Design Notes (Skeleton)

- Permission filtering happens **before** retrieval (see `retrieval.py`).
- LLM layer is currently a deterministic mock (`llm.py`) so you can run without API keys.
- Vector store is in-memory with simple keyword scoring. Replace with real embeddings + pgvector/Bedrock next.
- Auth is a simple API-key → role map. Designed so it can later map to real IdP group claims.

## Next Implementation Steps

1. Wire real embeddings and a persistent vector store.
2. Improve chunking and add metadata quality checks.
3. Build the evaluation question set and run baseline metrics.
4. Add Terraform for a minimal AWS deployment.
5. Flesh out the runbook with real operational steps.

---

See the `docs/` folder for the full engagement artifacts.
