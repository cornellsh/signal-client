# Configuration

!!! info "Who should read this"
    Consult this reference when you are configuring Signal Client for staging/production, tuning runtime limits, or wiring external services.

Signal Client reads configuration through the Pydantic `Settings` model (`signal_client.config.Settings`). Values can come from `SignalClient(config=...)`, environment variables, or `.env` files.

`Settings` merges several sections: core connectivity, API client behaviour, worker queue tuning, rate limiting, circuit breaking, storage, and dead-letter handling.

## Core Connectivity

| Setting | Env Var | Description |
| --- | --- | --- |
| `phone_number` | `SIGNAL_PHONE_NUMBER` | Bot phone number in E.164 format. |
| `signal_service` | `SIGNAL_SERVICE_URL` | Base URL of `signal-cli-rest-api` (JSON-RPC / WebSocket endpoint). |
| `base_url` | `SIGNAL_API_URL` | Base URL for REST API calls (`/v2/send`, `/v1/groups`, etc.). |
| `trust_all_certificates` | `SIGNAL_TRUST_ALL_CERTS` | Skip TLS verification (local testing only). |

## Worker & Queue Controls

| Setting | Default | Notes |
| --- | --- | --- |
| `worker_pool_size` | `4` | Number of concurrent workers consuming the queue. |
| `queue_size` | `1000` | Maximum items in the internal queue before producers block or drop. |
| `queue_put_timeout` | `1.0` | Seconds to wait for space in the queue before timing out. |
| `queue_drop_oldest_on_timeout` | `true` | When true, drop the oldest message on timeout instead of raising. |

## Rate Limiter

- `rate_limit`: Maximum operations allowed per period (default `50`).
- `rate_limit_period`: Period in seconds (default `1`).
- Metrics publish to the `rate_limiter_wait_seconds` histogram.

## Circuit Breaker

- `circuit_breaker_failure_threshold`: Consecutive failures before the breaker opens (default `5`).
- `circuit_breaker_reset_timeout`: Seconds to stay open before trying half-open (default `30`).
- `circuit_breaker_failure_rate_threshold`: Fraction of failures within the window that triggers the breaker (default `0.5`).
- `circuit_breaker_min_requests_for_rate_calc`: Minimum events before rate calculation applies (default `10`).
- States publish to the `circuit_breaker_state` gauge with labels `endpoint` and `state`.

## Dead Letter Queue

- `dlq_name`: Identifier used when persisting DLQ entries (default `signal_client_dlq`).
- `dlq_max_retries`: Attempts before parking a message (default `5`).
- Combine with the storage providers below to persist beyond process memory.

## Storage Providers

Signal Client ships SQLite and Redis adapters.

- `storage_type`: `sqlite` (default) or `redis`.
- `sqlite_database`: Path for SQLite (default `signal_client.db`).
- `redis_host`: Host or URL to Redis.
- `redis_port`: Port for Redis (positive integer).

## Example Configuration

```python
from signal_client import SignalClient

client = SignalClient(
    {
        "phone_number": "+15558675309",
        "signal_service": "https://signal-gateway.internal",
        "base_url": "https://signal-gateway.internal",
        "worker_pool_size": 8,
        "queue_size": 500,
        "queue_put_timeout": 2.0,
        "queue_drop_oldest_on_timeout": False,
        "rate_limit": 20,
        "rate_limit_period": 60,
        "circuit_breaker_failure_threshold": 8,
        "circuit_breaker_reset_timeout": 45,
        "storage_type": "redis",
        "redis_host": "redis.internal",
        "redis_port": 6379,
        "dlq_max_retries": 6,
    }
)
```

Missing required values raise detailed `ValidationError`s listing absent environment variables and expected types. See [Observability](./observability.md) for metrics details and [Operations](./operations.md) for scaling guidance.

---

**Next up:** Wire metrics and structured logs via [Observability](./observability.md) or plan your rollout with [Operations](./operations.md).
