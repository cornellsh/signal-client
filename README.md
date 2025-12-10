# signal-client

[![PyPI version](https://img.shields.io/pypi/v/signal-client)](https://pypi.org/project/signal-client/)
[![Python versions](https://img.shields.io/pypi/pyversions/signal-client)](https://pypi.org/project/signal-client/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://cornellsh.github.io/signal-client/)

Async Python framework for resilient Signal bots. Build fast on [`bbernhard/signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api) with typed helpers, resilient ingestion, and observability baked in.

## Table of Contents

-   [Features](#features)
-   [Quick Start](#quick-start)
    -   [1. Prerequisites](#1-prerequisites)
        -   [Setting up `signal-cli-rest-api` with Docker](#setting-up-signal-cli-rest-api-with-docker)
            -   [Option A: Using Docker Run](#option-a-using-docker-run)
            -   [Option B: Using Docker Compose](#option-b-using-docker-compose)
        -   [Environment Variables](#environment-variables)
    -   [2. Install](#2-install)
    -   [3. Create a Bot](#3-create-a-bot)
    -   [4. Run It](#4-run-it)
-   [Documentation](#documentation)
-   [Contributing](#contributing)
-   [License](#license)

## Features

-   **Resilience First:** Backpressure, DLQ retries, and rate/circuit breakers keep handlers stable during bursts.
-   **Typed Context Helpers:** Replies, reactions, attachments, locks, and receipts all live on one ergonomic context.
-   **Operations Ready:** Health and metrics servers, structured logging with PII redaction, and storage options (memory, SQLite, Redis).

## Quick Start

### 1. Prerequisites

Before you begin, ensure you have the following:

-   A Signal phone number that has been registered with `signal-cli`.
-   A running instance of the [`bbernhard/signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api`).

### Setting up `signal-cli-rest-api` with Docker

To use `signal-client`, you need a running instance of `signal-cli-rest-api`. This section outlines how to set it up using Docker.

First, create a directory on your host system to store the `signal-cli` configuration, ensuring persistence across container restarts:
```bash
mkdir -p $HOME/.local/share/signal-api
```

#### Option A: Using Docker Run

1.  **Pull the Docker Image:**
    ```bash
    docker pull bbernhard/signal-cli-rest-api
    ```

2.  **Run the Container:**
    ```bash
    docker run -d -p 8080:8080 -v $HOME/.local/share/signal-api:/home/.local/share/signal-cli bbernhard/signal-cli-rest-api
    ```

3.  **Register or Link your Signal Number with the API:**
    After starting the container, you need to register or link your Signal number with the `signal-cli-rest-api` instance. This typically involves:
    *   Opening `http://localhost:8080/v1/qrcodelink?device_name=signal-api` in your browser to scan a QR code from your mobile Signal app (for linking as a secondary device).
    *   Alternatively, for new registrations, initiating registration via `http://localhost:8080/v1/register/<YOUR_PHONE_NUMBER>` and then verifying with a received code via `http://localhost:8080/v1/verify/<YOUR_PHONE_NUMBER>/<YOUR_VERIFICATION_CODE>`.
    For detailed steps, refer to the [official `signal-cli-rest-api` documentation](https://github.com/bbernhard/signal-cli-rest-api).

#### Option B: Using Docker Compose

For a more robust setup, create a `docker-compose.yml` file:

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

3.  **Register or Link your Signal Number with the API:**
    Similar to the Docker Run option, you will need to register or link your Signal number with this `signal-cli-rest-api` instance. Follow the same procedure as described in "Option A: Using Docker Run" step 3, adapting the host and port if you changed them in your `docker-compose.yml`.
    For detailed steps, refer to the [official `signal-cli-rest-api` documentation](https://github.com/bbernhard/signal-cli-rest-api).

### Environment Variables

Finally, export these environment variables, pointing to your running `signal-cli-rest-api` instance:
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
