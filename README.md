# Signal Client

[![PyPI version](https://img.shields.io/pypi/v/signal_client.svg)](https://pypi.org/project/signal_client/)
[![Python versions](https://img.shields.io/pypi/pyversions/signal_client.svg)](https://pypi.org/project/signal_client/)
[![License](https://img.shields.io/pypi/l/signal_client.svg)](https://github.com/cornellshakh/signal_client/blob/main/LICENSE)

An asynchronous Python framework for building Signal bots.

## Core Abstractions

- **`SignalClient`**: The main bot client. Manages the service lifecycle and command registration.
- **`Command`**: A protocol for defining command handlers.
- **`Context`**: An object passed to handlers, providing a high-level API for message responses (e.g., `reply`, `react`).

## Technical Specification

This library uses a decoupled, service-oriented architecture with an async message queue for processing. For a complete architectural breakdown, see the **[Technical Architecture Specification](./docs/README.md)**.

## Installation

```bash
pip install signal_client
```

## Example

```python
import os
import asyncio
import logging
from signal_client import SignalClient, Command, Context

logging.basicConfig(level=logging.INFO)

class PingCommand(Command):
    """A command that replies with 'Pong'."""
    triggers = ["!ping"]

    async def handle(self, c: Context) -> None:
        await c.reply("Pong")

if __name__ == "__main__":
    signal_service = os.environ["SIGNAL_SERVICE"]
    phone_number = os.environ["PHONE_NUMBER"]

    bot = SignalClient({
        "signal_service": signal_service,
        "phone_number": phone_number,
    })

    bot.register(PingCommand())
    asyncio.run(bot.start())
```

## Runtime Dependencies

This library requires a running instance of `signal-cli-rest-api`.

1.  **Run the API**:

    ```bash
    docker run -p 8080:8080 \
        -v $(pwd)/signal-cli-config:/home/.local/share/signal-cli \
        -e 'MODE=json-rpc' bbernhard/signal-cli-rest-api:latest
    ```

2.  **Configure Environment**:

    ```bash
    export SIGNAL_SERVICE="127.0.0.1:8080"
    export PHONE_NUMBER="+YourSignalNumber"
    ```

3.  **Run Bot**:
    ```bash
    python your_bot_script.py
    ```

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

- **Dev Install**: `poetry install --with dev`
- **Tests**: `poetry run pytest`
- **Formatting**: `poetry run black .` and `poetry run ruff .`

## License

MIT
