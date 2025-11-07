---
title: Observability
summary: Instrument Signal Client with metrics, logs, and alerts your operations team can trust.
order: 13
---

## Metrics

| Metric | Type | Purpose |
| --- | --- | --- |
| `signal_client_messages_total` | Counter | Counts messages sent, grouped by command and outcome. |
| `signal_client_latency_seconds` | Histogram | Tracks end-to-end processing latency per worker. |
| `signal_client_dlq_total` | Counter | Records failures routed to the DLQ. |
| `signal_client_story_events_total` | Counter | Observes story publish activity.

!!! tip "Scrape configuration"
    Expose metrics on `http://<host>:${SIGNAL_CLIENT_METRICS_PORT}/metrics` and add the endpoint to Prometheus, Grafana Agent, or your hosted equivalent.

[=30% "Metrics endpoint online"]

## Structured logging

- Uses `structlog` JSON renderer with fields: `event`, `command`, `signal_number`, `trace_id`.
- Set `LOG_LEVEL=debug` to inspect payload flow during incident response.
- Forward logs to your central platform (Loki, Datadog, Splunk) with filter on `event="message.sent"`.

!!! info "Add correlation IDs"
    Pass `--trace-id` from upstream systems to tie Signal messages back to customer events or workflows.

[=60% "Logs enriched"]{: .warning}

## Alerts and dashboards

/// details | Recommended alerts
- High DLQ rate (>5% over 10 minutes)
- Latency p95 > 2 seconds for five consecutive scrapes
- REST bridge unresponsive for >60 seconds
///

/// details | Dashboard starter kit
- Message throughput over time with filters per command.
- Top failing commands, grouped by exception type.
- In-flight jobs vs worker concurrency.
///

!!! danger "Page the team when DLQ spikes"
    Failing to drain the DLQ quickly can lead to duplicated messages when the bridge resumes. Alert early and pause automation if the queue grows faster than recovery tasks.

[=100% "Observability ready"]{: .success}

> **Next step** · Learn how to run upgrades and incident response in [Operations](operations.md).
