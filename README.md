# Python Signal Client

A Python library for building bots and automating interactions with the Signal messaging platform. This library provides a high-level, asynchronous API for receiving messages, processing commands, and sending replies.

It is designed to work with the [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api).

## Features

- **Command-based:** Easily define and register commands with simple triggers.
- **Asynchronous:** Built on `asyncio` for high performance.
- **Extensible:** Cleanly structured with dependency injection for easy customization.
- **High-level API:** Simple `Context` object for replying, reacting, and sending messages.

## Getting Started

### Installation

```bash
pip install signal-client
```

_(Note: This is a placeholder for the actual package name if it were published.)_

### Quick Example

Here is a simple "ping-pong" bot:

```python
# main.py
import asyncio
from signal_client import SignalClient, Command, Context

# 1. Define a command
class PingCommand:
    triggers = ["!ping"]
    async def handle(self, context: Context) -> None:
        await context.reply("Pong!")

# 2. Configure and run the client
async def main():
    CONFIG = {
        "signal_service": "http://localhost:8080",
        "phone_number": "+1234567890", # Your bot's number
    }
    client = SignalClient(CONFIG)
    client.register(PingCommand())
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
```

## Full Documentation

For a complete guide to the library's architecture, core concepts, and a full API reference, please see our **[Comprehensive Documentation](./docs/README.md)**.
