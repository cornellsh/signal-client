---
title: Recipes
summary: Step-by-step playbooks for common Signal Client automations.
order: 210
---

## Encrypted attachments broadcast

[=25% "Upload media"]

1. Use `signal-client attachments upload outage.pdf` to capture a handle.
2. Store the handle in Redis keyed by incident ID.
3. Send a templated message to your broadcast groups with the handle.

/// details | Deep dive
- Validate recipients against an allowlist before sending.
- Rotate attachments after each incident so outdated data is not reused.
///

[=100% "Customers notified"]{: .success}

## Group escalation workflow

[=20% "Acknowledge alert"]

1. Command acknowledges the incoming alert and posts to the escalation group.
2. Secondary command pings on-call personnel until someone reacts with ✅.
3. Use `signal-client groups remove-member` for responders who hand off the incident.

/// details | Deep dive
- Track active responders in SQLite with expiry timestamps.
- Use Prometheus alerts to trigger fallback channels if no acknowledgement is received.
///

## Compliance survey

[=40% "Survey deployed"]

1. Schedule APScheduler job that enqueues a `compliance_survey` command daily.
2. Command sends a multiple-choice message and stores selections in SQLite.
3. Export aggregate results via webhook to your BI system.

/// details | Deep dive
- Provide a REST endpoint for manual resends when employees miss the window.
- Map responses to employee IDs using dependency-injected HR data.
///

## Story campaign

[=50% "Story ready"]

1. Render campaign artwork and upload via REST `/v1/stories` endpoint.
2. Command schedules a series of story releases using APScheduler.
3. Monitor `signal_client_story_events_total` for delivery success.

/// details | Deep dive
- Use a staging device to preview stories before publishing.
- Sync schedule with marketing calendar to avoid conflicting pushes.
///

## Incident postmortem reminder

[=30% "Reminder scheduled"]

1. After incident closure, enqueue delayed job with due timestamp.
2. Command pings the incident owner with structured checklist and link to runbook.
3. If no response after 24 hours, escalate to the team's manager via broadcast.

/// details | Deep dive
- Use `context.metrics.counter("postmortem_escalations").inc()` to track repeated misses.
- Store incident metadata in Redis to avoid duplicate reminders.
///

> **Next step** · Reference the sample scripts under [`scripts/`](../scripts/) for more end-to-end automation examples.

~{Key management flow}(key-management.json)
