# Quickstart

!!! info "Who should read this"
    Follow this guide if you want to stand up Signal Client locally, link it to `signal-cli-rest-api`, and verify the runtime end-to-end.

This guide links `signal-cli-rest-api`, installs Signal Client, and deploys a simple command using the actual runtime APIs.

## 1. Launch `signal-cli-rest-api`

1. Create a config directory to persist your registration:

   ```bash
   mkdir -p signal-cli-config
   ```

2. Launch the REST API in normal mode and link a device:

   ```bash
   docker run -p 8080:8080 \
     -v "$(pwd)/signal-cli-config:/home/.local/share/signal-cli" \
     -e MODE=normal bbernhard/signal-cli-rest-api:latest
   ```

   Open `http://127.0.0.1:8080/v1/qrcodelink?device_name=signal-client` and scan the QR code from Signal on your phone.

3. Restart the container in JSON-RPC mode (faster and required for streaming updates):

   ```bash
   docker run -p 8080:8080 \
     -v "$(pwd)/signal-cli-config:/home/.local/share/signal-cli" \
     -e MODE=json-rpc bbernhard/signal-cli-rest-api:latest
   ```

## 2. Install Signal Client & Verify Compatibility

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install signal-client
python -m signal_client.compatibility --strict
```

The compatibility guard exits non-zero when a dependency (aiohttp, dependency-injector, structlog, pydantic, etc.) falls outside the supported range. `--strict` treats warnings (e.g., upcoming deprecations) as failures during setup.

## 3. Scaffold Your Project

You can use any tooling; here’s a plain `pip` flow:

```bash
mkdir dad-joke-bot
cd dad-joke-bot
python3 -m venv .venv
source .venv/bin/activate
pip install signal-client python-dotenv
```

Create `.env` to store configuration:

```env
SIGNAL_PHONE_NUMBER=+1234567890
SIGNAL_SERVICE_URL=http://localhost:8080
SIGNAL_API_URL=http://localhost:8080
```

## 4. Implement a Command

```python
# commands/joke.py
import random

from signal_client import Context, command
from signal_client.infrastructure.schemas.requests import SendMessageRequest

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "What do you call a fake noodle? An impasta!",
    "Did you hear about the claustrophobic astronaut? He just needed a little space.",
]


@command("!joke", "!dad", description="Send a random dad joke.")
async def joke(context: Context) -> None:
    await context.reply(
        SendMessageRequest(message=random.choice(JOKES), recipients=[])
    )
    await context.react("😂")
```

## 5. Wire Signal Client

```python
# main.py
import asyncio
import os

from dotenv import load_dotenv

from signal_client import SignalClient
from commands.joke import joke


async def main() -> None:
    load_dotenv()
    client = SignalClient(
        {
            "phone_number": os.environ["SIGNAL_PHONE_NUMBER"],
            "signal_service": os.environ["SIGNAL_SERVICE_URL"],
            "base_url": os.environ["SIGNAL_API_URL"],
            "worker_pool_size": 4,
            "queue_size": 200,
        }
    )

    client.register(joke)

    async with client:
        await client.start()


if __name__ == "__main__":
    asyncio.run(main())
```

## 6. Observe Metrics & Logs

Expose the Prometheus endpoint in your host app:

```python
from prometheus_client import start_http_server

start_http_server(9102)
```

- Visit `http://localhost:9102/metrics` to confirm `message_queue_depth`, `message_queue_latency_seconds`, and `messages_processed_total`.
- Structured logs include worker IDs, command names, queue latency, and DLQ actions. Configure structlog in your host app before creating `SignalClient` if you need custom processors.

## 7. Run & Test

```bash
SIGNAL_PHONE_NUMBER=+1234567890 SIGNAL_SERVICE_URL=http://localhost:8080 SIGNAL_API_URL=http://localhost:8080 python main.py
```

Send `!joke` from a different Signal device—your bot replies instantly.

Run your tests whenever you iterate:

```bash
pytest
```

Ready to go deeper? Explore [Architecture](./architecture.md) to understand the worker pipeline or [Operations](./operations.md) to prepare for production incidents.

---

**Next up:** Review the [Feature Tour](./feature-tour.md) for a visual map of the services or jump ahead to [Configuration](./configuration.md) to tune the runtime.
