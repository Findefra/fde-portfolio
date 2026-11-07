# 05 — Runbook

## Overview

This runbook describes how to operate the Ops Knowledge Assistant in its pilot form. It is written so another engineer on the platform team can start, stop, diagnose, and extend the system without tribal knowledge.

## Prerequisites

- Access to the AWS account / environment where the service is deployed
- Terraform (or the IaC used) and appropriate credentials
- Ability to reach the service endpoint
- Knowledge of the current role claims / API keys in use

## Starting and Stopping

*To be completed once deployment exists.*

- How to apply / destroy infrastructure
- How to restart the application service
- Health check endpoint and expected response

## Common Operations

### Adding or updating documents
1. Place new/updated files in the designated corpus location with correct metadata.
2. Run the ingestion job.
3. Verify the new chunks appear in the vector store.
4. Re-run a subset of evaluation questions that touch the new content.

### Rotating credentials / API keys
*To be filled.*

### Checking logs and metrics
*To be filled (CloudWatch / equivalent).*

## Common Failures and Responses

| Symptom | Likely Cause | First Actions |
|---------|--------------|---------------|
| Service returns 5xx | Application crash or dependency down | Check health, logs, database connectivity |
| Empty or low-quality answers | Ingestion issue or retrieval filter too aggressive | Check recent ingestion, test retrieval directly |
| Permission errors / unexpected refusals | Role claim missing or metadata mis-tagged | Verify incoming role header and document metadata |
| High latency | Cold start, large context, or LLM throttling | Check token counts and provider status |

## Escalation

- Who owns the service in the pilot phase
- When to involve security (permission leakage concerns)
- How to disable the service quickly if needed

## Notes

Keep this document updated as real operational experience is gained. A runbook that does not match reality is worse than no runbook.
