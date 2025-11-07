# Operations

!!! info "Who should read this"
    Reference these runbooks when you are operating Signal Client in staging/production or preparing for incident response.

Runbooks and procedures for keeping Signal Client deployments healthy.

## Monitor Queue Pressure

1. Watch `message_queue_depth` and `message_queue_latency_seconds` for rising trends.
2. Review logs for warnings tagged with `queue_latency`.
3. Mitigation options:
   - Increase `worker_pool_size` cautiously (see below).
   - Reduce incoming triggers or disable non-critical commands if the queue stays saturated.
   - Replay the DLQ after dependencies stabilise.

## Scale Worker Pool

1. Evaluate current load and rate-limiter wait times.
2. Bump `worker_pool_size` in small increments and redeploy.
3. Validate that `rate_limiter_wait_seconds` stays acceptable; adjust `rate_limit` / `rate_limit_period` if necessary.
4. Confirm host resource limits (FDs, CPU) are sufficient.

## Rotate Credentials

1. Pause ingestion (`SignalClient.shutdown()` or drain queue).
2. Export/inspect DLQ to ensure critical messages are handled.
3. Rotate secrets via your provider (Vault, AWS Secrets Manager, etc.).
4. Restart process; compatibility guard runs automatically at boot.
5. Monitor logs for authentication errors post-rotation.

## Replay the Dead Letter Queue

1. Check `dead_letter_queue_depth` gauge and logs for parked messages.
2. Validate upstream availability.
3. Inspect payloads (ensure the process has the same configuration environment variables used in production):
   ```bash
   python -m signal_client.cli
   ```
4. Reinject critical messages manually (for example, via a maintenance script) once dependencies recover.
5. Monitor queue depth/latency; repeat until backlog is cleared.

## Release Checklist

1. CI must pass lint (`ruff`), format (`black`), type-check (`mypy`), tests (`pytest-safe`), security audit (`pip-audit`), docs build (MkDocs), and `release-guard`.
2. For pre-1.0 versions, inspect commits for `!` or `BREAKING CHANGE` markers before publishing.
3. Build artifacts via `poetry build`; verify contents if distributing privately.
4. Rollbacks: revert the commit, rerun CI, and publish a corrective release.

## Incident Response Quick Links

- **Compatibility guard failure:** `python -m signal_client.compatibility --json`
- **Circuit breaker stuck open:** inspect `circuit_breaker_state` and logs for failing endpoints.
- **High rate limiter wait:** adjust quotas or the configured rate limiter period.
- **Metrics offline:** ensure Prometheus exporter is running and the metrics endpoint is exposed.

For additional context on telemetry, see [Observability](./observability.md). Configuration details live in [Configuration](./configuration.md).

---

**Next up:** Explore the [API Reference](./api-reference.md) for tooling that supports these runbooks, or return to the [Use Cases](./use-cases.md) page to see how teams combine these practices.
