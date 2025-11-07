---
title: Use Cases
summary: Proven workflows Signal Client unlocks out of the box.
order: 2
---

## Core scenarios

| Workflow | Goal | Why Signal Client |
| --- | --- | --- |
| Customer support triage | Route inbound Signal chats to specialists with context enrichment. | Async command chain with structured hand-offs and Prometheus metrics. |
| Outage broadcasts | Deliver rapid status updates with attachments to internal teams. | Attachment caching, retry policies, and story sends across segments. |
| Compliance attestations | Collect daily confirmations from distributed devices. | Typed forms, persistent DLQ, and audit events per response. |

/// caption
Signal Client playbooks ready for launch
///

## Scenario spotlights

/// details | Customer support automation
- Ingest messages via webhook forwarding or batched receive.
- Enrich payloads with CRM fields using dependency-injected services.
- Use multi-step commands to acknowledge, assign, and resolve conversations.
///

/// details | Broadcast alerts
- Render status templates in the container, attach PDFs or screenshots, and push to critical groups.
- Track delivery metrics with built-in Prometheus counters and expose dashboards to on-call engineers.
- Schedule follow-up pings or fallbacks when acknowledgements are missing.
///

/// details | Compliance attestations
- Configure reminder cadence through APScheduler-backed jobs.
- Persist responses in SQLite/Redis and escalate to ops channels if deadlines pass.
- Sync daily outcome summaries via webhooks to enterprise systems.
///

!!! tip "Need a custom workflow?"
    Use the [Guides](guides/writing-async-commands.md) section to extend Signal Client with bespoke commands, schedulers, or outbound integrations.

> **Next step** · Tour the major runtime features in [Feature Tour](feature-tour.md).
