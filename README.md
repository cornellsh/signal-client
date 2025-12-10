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

- A Signal phone number registered.
- A running [`bbernhard/signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api) instance.

#### Setting up `signal-cli-rest-api` with Docker

1.  **Pull the Docker Image:**
    ```bash
    docker pull bbernhard/signal-cli-rest-api
    ```

2.  **Run the Container:**
    ```bash
    docker run -d -p 8080:8080 -v /path/to/your/data:/app/data bbernhard/signal-cli-rest-api
    ```
    Replace `/path/to/your/data` with the actual path on your host machine where you want to store `signal-cli` data (e.g., `/home/user/signal-cli-data`). This ensures your registration and message history persist across container restarts.



    For more details on registration and usage, refer to the [official `signal-cli-rest-api` documentation](https://github.com/bbernhard/signal-cli-rest-api).

##### Alternative: Using Docker Compose

For a more robust setup, you can use `docker-compose`. Create a `docker-compose.yml` file like this:

```yaml
version: "3"
services:
  signal-cli-rest-api:
    image: bbernhard/signal-cli-rest-api:latest
    environment:
      - MODE=native #supported modes: json-rpc, native, normal
      #- AUTO_RECEIVE_SCHEDULE=0 22 * * * #enable this parameter on demand (see description below)
    ports:
      - "8080:8080" #map docker port 8080 to host port 8080.
    volumes:
      - "./signal-cli-config:/home/.local/share/signal-cli" #map "signal-cli-config" folder on host system into docker container. the folder contains the password and cryptographic keys when a new number is registered
```

Then run `docker-compose up -d` in the same directory as your `docker-compose.yml`.

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
