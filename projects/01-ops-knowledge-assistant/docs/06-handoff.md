# 06 — Handoff

## What Is Being Delivered

- Working permission-aware knowledge assistant (API)
- Curated pilot corpus with metadata
- Evaluation set and recorded results
- Terraform (or IaC) for the supporting infrastructure
- Documentation set (discovery → scope → architecture → evaluation → runbook)
- Short demo recording (to be added)

## What the Receiving Team Gets

1. Ability to ask operational questions and receive cited answers or clear refusals.
2. Visibility into accuracy and permission behavior via the evaluation report.
3. A system that can be started, stopped, and lightly extended using the runbook.
4. Explicit list of known limitations and recommended next steps.

## Recommended Next Steps (Post-Pilot)

- Map the simple role claims to real identity provider groups.
- Expand the corpus with additional high-value document sources.
- Add continuous or scheduled re-ingestion for updated documents.
- Introduce a lightweight UI if API-only proves insufficient for adoption.
- Strengthen observability and alerting based on real usage patterns.
- Re-run evaluation after any significant change to retrieval or generation logic.

## Known Limitations at Handoff

*To be completed at the end of the pilot.*

## Ownership Transition

- Who currently owns the code and infrastructure
- Who will own ongoing document quality and metadata
- How future changes should be requested and reviewed

## Sign-off Checklist

- [ ] Evaluation results reviewed
- [ ] Runbook walkthrough completed with at least one other engineer
- [ ] Permission boundary tests passed (zero leakage observed)
- [ ] Infrastructure and secrets ownership clarified
- [ ] Demo available for stakeholders

---

This handoff is intentionally lightweight. The goal is a clean, honest transfer rather than a long formal report.
