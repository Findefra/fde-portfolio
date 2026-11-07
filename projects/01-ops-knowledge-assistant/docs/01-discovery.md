# 01 — Discovery

## Customer Context (Fictional)

**Organization:** Mid-size technology company with a dedicated Cloud Operations / Platform team (approx. 12–15 engineers).

**Current state:**
- Operational knowledge lives in multiple places: Confluence pages, S3 buckets containing PDFs and markdown, Git repositories with Terraform modules and READMEs, and scattered incident post-mortems.
- Engineers frequently ask the same questions in Slack or spend 10–20 minutes searching for the correct procedure.
- Some production runbooks and hardening exceptions are intentionally restricted to senior on-call or security-approved personnel.
- Outdated documents occasionally cause incorrect actions.

## Stated Problem

"We need one place where the team can ask operational questions and get trustworthy answers with sources, without people accidentally seeing things they shouldn't."

## Actual Problem (after discovery)

- Knowledge is fragmented and versioning is inconsistent.
- Access control is currently informal ("don't share this page").
- There is no reliable way to know whether an answer is current or complete.
- The team wants measurable improvement in time-to-answer and reduction of incorrect guidance, not just a chatbot.

## Key Stakeholders

- Platform / Cloud Ops engineering (primary users)
- Security / Compliance (access control and audit requirements)
- On-call rotation (high-urgency users)
- Engineering managers (success metrics and adoption)

## Constraints Discovered

- Data sensitivity: some documents contain internal network details, exception justifications, and production runbook steps.
- Role-based access is required; simple "logged-in" is insufficient.
- Preference for staying inside the existing AWS footprint.
- Cost sensitivity for embedding and generation calls.
- Must support clear refusal when evidence is weak or permission is missing.
- Team has limited bandwidth to maintain a complex new system.

## Initial Success Definition (to be refined in scope)

- Engineers can ask common operational questions and receive cited answers in seconds instead of minutes.
- Restricted content never appears for unauthorized roles.
- The system can be operated by the existing platform team with a clear runbook.
- Evaluation results are available so the team can see accuracy and refusal behavior before wider rollout.

## Open Questions

- Exact identity provider and group claims available?
- Preferred vector store and LLM endpoint (Bedrock vs external)?
- Which document sources are highest priority for the pilot corpus?
- Who will own ongoing document ingestion and metadata quality?

---

*This document should be updated as more is learned. Do not treat it as final until scope is signed off.*
