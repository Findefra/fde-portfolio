# 02 — Hardening / Change Agent (with Human Approval Gate)

**Status:** Planned  
**Type:** Tool-using agent for infrastructure findings + mandatory human approval before any change

## Customer Problem (Fictional Engagement)

A cloud operations / security team wants continuous visibility into configuration drift and missing controls (unencrypted volumes, missing required tags, overly permissive security groups, outdated AMIs, etc.). They are willing to let an agent *propose* remediation actions (Terraform snippets or AWS API calls) but will **never** allow unsupervised application of changes.

The agent must:
- Discover findings via AWS APIs (or realistic mocks)
- Propose minimal, well-explained changes
- Require explicit human approval before any state-changing action
- Maintain a clear audit trail of proposals and decisions

## Why This Project

This plays directly to Cloud Ops, Terraform, CIS hardening, and production safety strengths while demonstrating modern agent patterns, tool use, and guardrails that FDE interviews care about.

## Planned Structure

Same documentation and folder layout as Project 1:

```
02-hardening-agent/
├─ README.md
├─ docs/
│   ├─ 01-discovery.md
│   ├─ 02-scope.md
│   ├─ 03-architecture.md
│   ├─ 04-evaluation.md
│   ├─ 05-runbook.md
│   └─ 06-handoff.md
├─ src/
├─ terraform/
└─ evals/
```

## Current Progress

- [x] Skeleton created
- [ ] Discovery and scope
- [ ] Core agent loop + tools
- [ ] Approval gate implementation
- [ ] Evaluation focused on safe refusal and proposal quality
- [ ] Deployment and documentation

---

*This project will be started after Project 1 reaches a solid pilot state.*
