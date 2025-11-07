# Observability

!!! info "Who should read this"
    Use this guide when you need to wire metrics, logs, or diagnostics into your deployment pipeline or dashboards.

Signal Client surfaces rich telemetry and diagnostics to keep production bots healthy.

## Prometheus Metrics

Metrics are registered in `signal_client.metrics` and share a single Prometheus registry.

| Metric | Type | Labels | Description |
| --- | --- | --- | --- |
| `message_queue_depth` | Gauge | — | Current queue size. |
| `message_queue_latency_seconds` | Histogram | — | Time between enqueue and dequeue. |
| `messages_processed_total` | Counter | — | Messages processed successfully. |
| `errors_occurred_total` | Counter | — | Errors encountered during processing. |
| `dead_letter_queue_depth` | Gauge | `queue` | Pending DLQ messages. |
| `rate_limiter_wait_seconds` | Histogram | — | Time spent waiting for rate limiter permits. |
| `circuit_breaker_state` | Gauge | `endpoint`, `state` | Current state (`closed`, `open`, `half_open`). |
| `api_client_performance_seconds` | Histogram | — | Latency for REST API calls through the client. |

Export metrics using the standard Prometheus client:

```python
from prometheus_client import start_http_server

start_http_server(9102)
```

## Structured Logging

- Logging uses `structlog` with context variables.
- Each message binds `worker_id`, `command_name`, `queue_latency`, and `message_id`.
- Configure structlog in your host app before instantiating `SignalClient` if you need custom processors; the runtime skips configuration when structlog is already set up.

## Diagnostics

- `Settings.from_sources()` reports missing/invalid configuration with actionable errors.
- `compatibility.check_supported_versions()` throws on unsupported dependency versions; run it as part of CI to catch drifts early.
- The `pytest-safe` helper script runs tests without leaving background tasks alive.

## Instrumenting Custom Metrics

Signal Client uses the default Prometheus registry. Register your own collectors as usual:

```python
from prometheus_client import Gauge

active_rooms = Gauge("bot_active_rooms", "Tracked active rooms")
```

If you expose metrics via an ASGI/WSGI app instead of `start_http_server`, call `signal_client.metrics.render_metrics()` to obtain the exposition payload.

## Alerting Suggestions

- Alert when `message_queue_depth` stays near the queue limit for more than a minute.
- Alert when `circuit_breaker_state{state="open"}` is non-zero for critical endpoints.
- Alert on elevated `message_queue_latency_seconds` p95 or sustained growth in `dead_letter_queue_depth`.

For mitigation strategies, see the [Operations](./operations.md) runbooks.

---

**Next up:** Put these signals to work by following the [Operations](./operations.md) incident playbooks or explore the [API Reference](./api-reference.md) for customization hooks.
