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
├─ src/                 # Application code (FastAPI, ingestion, retrieval)
├─ terraform/           # Infrastructure
└─ evals/               # Evaluation questions and results
```

## Current Progress

- [x] Repository and documentation skeleton created
- [ ] Discovery and scope documents finalized
- [ ] Document corpus prepared and tagged
- [ ] Ingestion + vector store pipeline
- [ ] Permission-aware retrieval + citations
- [ ] Evaluation set and baseline metrics
- [ ] AWS deployment via Terraform
- [ ] Runbook and handoff complete

## How to Run (once implemented)

Instructions will be added here after the core service is working.

---

See the `docs/` folder for the full engagement artifacts.
