---
title: Production Secrets
summary: Safeguard Signal credentials, API keys, and runtime configuration.
order: 301
---

## Storage strategy

- Store the Signal credential bundle (`registration.yaml`) in an encrypted vault (HashiCorp Vault, AWS Secrets Manager).
- Mount secrets at runtime only; avoid baking them into container images.
- Leverage Kubernetes Secrets or AWS/GCP secret stores with auto-rotation.[^policy]

!!! danger "Never email credential backups"
    Email, chat, and shared drives are not acceptable storage mediums for Signal credentials. Use your organisation's secrets platform instead.

## Rotation cadence

| Secret | Rotation guidance |
| --- | --- |
| Signal credential bundle | Re-link quarterly or when personnel change. |
| Access tokens (REST bridge) | Rotate monthly; revoke immediately if exposed. |
| API keys for downstream integrations | Follow provider policy, but no longer than 90 days. |

## Access controls

/// details | Principle of least privilege
- Limit read access to CI/CD service accounts and the runtime identity.
- Require MFA for administrative access to secret stores.
- Log every secret retrieval for auditing.
///

/// details | Incident handling
- Revoke compromised Signal credentials using the official Signal app.
- Rotate downstream API keys and re-run `release-guard` before restarting automation.
- Notify stakeholders and review audit logs for abuse.
///

!!! note "Automate compliance"
    Use the `production_secrets` GitHub Action workflow to run policy checks on pull requests modifying secret templates.

> **Next step** · Review the privacy guarantees provided by the runtime in [TEE Privacy Architecture](tee_privacy_architecture.md).

[^policy]: Align rotation schedules with your organisation's security policy; the above are minimum recommendations.
