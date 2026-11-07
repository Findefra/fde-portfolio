# 02 — Scope (Pilot)

## In Scope for Pilot

- Ingestion of a curated corpus of operational documents (markdown, text, selected PDFs) with metadata (team, sensitivity, version, environment).
- Permission-aware retrieval: filter by user role **before** vector search.
- Answer generation with mandatory source citations.
- Explicit refusal path when retrieval confidence is low or permission is insufficient.
- Simple authentication mechanism that carries a role claim (API key + role for portfolio version; designed so it can later map to real IdP groups).
- Evaluation set of 30–50 questions covering answerable, unanswerable, and permission-boundary cases.
- Deployment on AWS using Terraform (or equivalent IaC notes).
- Basic observability (logs, health check, simple metrics).
- Runbook and handoff documentation so another engineer can operate the system.

## Explicitly Out of Scope (Pilot)

- Full SSO / real corporate IdP integration (will be designed for later).
- Real-time continuous ingestion from live Confluence or S3 (batch/manual for pilot is acceptable).
- Multi-turn conversational memory across long sessions.
- Automatic document update detection and re-embedding pipeline at scale.
- Frontend UI beyond a minimal API client or simple web form (API-first is fine).
- Advanced agentic tool use or multi-step workflows.
- Cost optimization beyond basic logging of token usage.
- High-availability multi-region setup.

## Acceptance Criteria for Pilot Completion

1. A working service that accepts a question + role and returns either a cited answer or a clear refusal.
2. Evaluation results documented with pass/fail rates for the defined question categories.
3. At least one demonstrated case of correct refusal on a restricted document.
4. Deployed (or fully reproducible via Terraform) on AWS with least-privilege IAM described.
5. Runbook exists that covers start/stop, common failures, and how to add new documents.
6. Architecture decisions and known limitations are written down.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Corpus quality is poor → low accuracy | Start with a small, high-quality curated set; document limitations honestly |
| Permission model is too simplistic | Design metadata and filter so it can later map to real groups |
| Cost of embeddings/LLM is higher than expected | Log token usage; prefer smaller models for pilot; keep corpus modest |
| Scope creep into full platform | Strict out-of-scope list above; time-box |

## Timeline Target (Internal)

Aim to complete the pilot artifacts (working system + docs + eval) within 4–6 focused weeks.
