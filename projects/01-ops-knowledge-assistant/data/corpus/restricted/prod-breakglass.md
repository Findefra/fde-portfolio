# Production Break-Glass Procedure (Restricted)

**Sensitivity: Restricted — Senior SRE / On-call Lead only**

## When to use
Only during a confirmed Sev-1 incident when normal access paths are unavailable or too slow.

## Steps
1. Declare the incident in the incident channel and obtain verbal approval from the incident commander.
2. Use the designated break-glass IAM role (name and account are recorded in the secure vault, not here).
3. Log the session start time, ticket number, and justification.
4. Perform the minimum actions required to restore service.
5. Terminate the session and complete the post-incident access review within 24 hours.

## Prohibited
- Using break-glass for convenience or non-incident work
- Sharing the role credentials
- Leaving long-lived sessions open

Unauthorized use is a security incident.
