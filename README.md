# signal-client

[![PyPI version](https://img.shields.io/pypi/v/signal-client)](https://pypi.org/project/signal-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://cornellsh.github.io/signal-client/)

**Async Python framework for production-ready Signal bots.**

Builds on [`bbernhard/signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api) with typed helpers, resilient ingestion, backpressure, DLQ retries, rate limiting, and observability.

## Features

- Async message ingestion with backpressure and dead letter queue
- Typed context helpers for replies, reactions, attachments, locks, and receipts
- Rate limiting and circuit breakers for API stability
- Health and metrics endpoints with Prometheus
- Structured logging with PII redaction
- Storage backends: memory, SQLite, or Redis

## Quick Start

```bash
# Install
pip install signal-client

# Run signal-cli-rest-api
docker run -d -p 8080:8080 \
  -v $HOME/.local/share/signal-api:/home/.local/share/signal-cli \
  -e 'MODE=native' \
  bbernhard/signal-cli-rest-api

# Register your Signal number
# Scan QR at: http://localhost:8080/v1/qrcodelink?device_name=signal-api
# Or register at: http://localhost:8080/v1/register/<YOUR_PHONE_NUMBER>

# Configure environment
export SIGNAL_PHONE_NUMBER="+15551234567"
export SIGNAL_SERVICE_URL="http://localhost:8080"
export SIGNAL_API_URL="http://localhost:8080"
```

```python
import asyncio
from signal_client import SignalClient, command

@command("!ping")
async def ping(ctx):
    await ctx.reply_text("pong")

async def main():
    bot = SignalClient()
    bot.register(ping)
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

Configuration loads from environment variables and `.env` files. Use `SIGNAL_` prefixes for all settings.

### Required Settings

| Env Var | Description | Default |
|----------|-------------|----------|
| `SIGNAL_PHONE_NUMBER` | Your Signal phone number | - |
| `SIGNAL_SERVICE_URL` | Signal service URL | - |
| `SIGNAL_API_URL` | Signal API URL | - |

### API Settings

| Env Var | Description | Default |
|----------|-------------|----------|
| `SIGNAL_API_TOKEN` | API authentication token | - |
| `api_retries` | Retry attempts on transient errors | `3` |
| `api_backoff_factor` | Exponential backoff factor | `0.5` |
| `api_timeout` | API request timeout (seconds) | `30` |

### Queue and Worker Settings

| Env Var | Description | Default |
|----------|-------------|----------|
| `queue_size` | Maximum queued messages | `1000` |
| `worker_pool_size` | Concurrent worker tasks | `4` |
| `queue_put_timeout` | Queue put timeout (seconds) | `1.0` |
| `durable_queue_enabled` | Enable persistent queueing | `false` |
| `durable_queue_max_length` | Maximum durable queue length | `10000` |

### Rate Limiting

| Env Var | Description | Default |
|----------|-------------|----------|
| `rate_limit` | Max requests per period | `50` |
| `rate_limit_period` | Rate limit window (seconds) | `1` |

### Circuit Breaker

| Env Var | Description | Default |
|----------|-------------|----------|
| `circuit_breaker_failure_threshold` | Failures before opening | `5` |
| `circuit_breaker_reset_timeout` | Reset timeout (seconds) | `30` |
| `circuit_breaker_failure_rate_threshold` | Failure rate threshold (0.0-1.0) | `0.5` |

### Storage

| Env Var | Description | Default |
|----------|-------------|----------|
| `storage_type` | Backend: `memory`, `sqlite`, or `redis` | `memory` |
| `redis_host` | Redis host | `localhost` |
| `redis_port` | Redis port | `6379` |
| `sqlite_database` | SQLite database file | `signal_client.db` |

### Dead Letter Queue

| Env Var | Description | Default |
|----------|-------------|----------|
| `dlq_name` | DLQ name in storage | `signal_client_dlq` |
| `dlq_max_retries` | Maximum DLQ retries | `5` |

### Logging

| Env Var | Description | Default |
|----------|-------------|----------|
| `log_redaction_enabled` | Enable PII redaction | `true` |

## Documentation

Full guides, examples, and API references at [cornellsh.github.io/signal-client](https://cornellsh.github.io/signal-client/).

## Contributing

```bash
# Set up development environment
poetry install

# Enable pre-commit hooks
poetry run pre-commit install
```

## License

MIT License - see [LICENSE](LICENSE).
