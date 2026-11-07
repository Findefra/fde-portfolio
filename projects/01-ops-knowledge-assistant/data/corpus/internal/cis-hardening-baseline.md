# CIS Hardening Baseline (Internal)

## Scope
This baseline applies to all Linux AMIs built via EC2 Image Builder for production workloads.

## Required Controls
- Disable root SSH login
- Enforce MFA for console access where applicable
- Ensure CloudWatch agent is installed and shipping logs
- Apply security updates within 7 days of release for critical CVEs
- Tag all resources with Environment, Owner, and CostCenter

## Exceptions
Temporary exceptions must be recorded in the exception register and reviewed every 90 days.
Only Security and senior Platform engineers may approve exceptions.

## Related Runbooks
See the AMI rebuild and ASG rolling update procedures for implementation details.
