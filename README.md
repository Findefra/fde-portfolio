# FDE Portfolio

**Forward Deployed Engineer engagement simulations**

This repository contains production-style projects that demonstrate the full FDE loop:

- Customer discovery and scoping under ambiguity
- Design decisions with explicit trade-offs
- Working systems that integrate, deploy, and handle real constraints
- Evaluation with honest metrics and failure analysis
- Runbooks and handoff documentation

These are framed as fictional customer engagements (or sanitized real patterns) so they can be shared publicly while still reflecting the judgment required in the role.

## Projects

| Project | Status | Focus |
|---------|--------|-------|
| [01 - Ops Knowledge Assistant](./projects/01-ops-knowledge-assistant/) | In Progress | Permission-aware RAG over operational docs, citations, role-based access, evaluation, AWS deployment |
| [02 - Hardening / Change Agent](./projects/02-hardening-agent/) | Planned | Agent that proposes infrastructure remediation with mandatory human approval gate |

## How to navigate

Each project follows the same structure:

```
projects/<name>/
├─ README.md              # Customer problem + how to run
├─ docs/
│   ├─ 01-discovery.md
│   ├─ 02-scope.md
│   ├─ 03-architecture.md
│   ├─ 04-evaluation.md
│   ├─ 05-runbook.md
│   └─ 06-handoff.md
├─ src/                   # Application code
├─ terraform/             # Infrastructure as code
└─ evals/                 # Evaluation sets and results
```

## Principles used across projects

- Write discovery and scope documents **before** heavy coding
- Prefer constrained, honest systems over ambitious incomplete ones
- Document failures and limitations deliberately
- Show production qualities: auth, least privilege, observability, retries, cost awareness
- Package like a real deliverable so another engineer could operate it

## Owner

Cloud Operations Engineer building toward Forward Deployed Engineering roles.
Strong background in AWS, Terraform, automation, security hardening, and production reliability.

---

*This portfolio is actively under construction. Project 1 is the current focus.*
