# signal-client

[![PyPI version](https://img.shields.io/pypi/v/signal-client)](https://pypi.org/project/signal-client/)
[![Python versions](https://img.shields.io/pypi/pyversions/signal-client)](https://pypi.org/project/signal-client/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://cornellsh.github.io/signal-client/)

Async Python framework for resilient Signal bots. Build fast on [`bbernhard/signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api) with typed helpers, resilient ingestion, and observability baked in.

## Features

- **Resilience First:** Backpressure, DLQ retries, and rate/circuit breakers keep handlers stable during bursts.
- **Typed Context Helpers:** Replies, reactions, attachments, locks, and receipts all live on one ergonomic context.
- **Operations Ready:** Health and metrics servers, structured logging with PII redaction, and storage options (memory, SQLite, Redis).

## Quick Start

### 1. Prerequisites

- A Signal phone number registered with `signal-cli`.
- A running [`bbernhard/signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api) instance.
- Export these environment variables:
  ```bash
  export SIGNAL_PHONE_NUMBER="+15551234567"
  export SIGNAL_SERVICE_URL="http://localhost:8080"
  export SIGNAL_API_URL="http://localhost:8080"
  ```

### 2. Install

```bash
# Using poetry
poetry add signal_client

# Using pip
pip install signal-client
```

### 3. Create a Bot

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

### 4. Run It

```bash
python your_bot_file.py
```

## Documentation

For full guides, examples, and API references, see the **[official docs site](https://cornellsh.github.io/signal-client/)**.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

- Set up your development environment with `poetry install`.
- Activate pre-commit hooks with `poetry run pre-commit install`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
