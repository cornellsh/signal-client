# Signal Client

[![CI](https://github.com/cornellsh/signal-client/actions/workflows/ci.yml/badge.svg)](https://github.com/cornellsh/signal-client/actions/workflows/ci.yml)
[![License](https://img.shields.io/pypi/l/signal_client.svg)](https://github.com/cornellsh/signal_client/blob/main/LICENSE)

## Quickstart

1. **Connect to `signal-cli-rest-api`.** Pair your bot account, enable JSON-RPC mode, and leave it running so the runtime can reach it.
2. **Install and verify the runtime.**
   ```bash
   pip install signal-client
   python -m signal_client.compatibility --strict
   ```
3. **Register a simple command.**
   ```python
   import asyncio
   from signal_client.bot import SignalClient
   from signal_client.context import Context
   from signal_client.command import Command
   from signal_client.infrastructure.schemas.requests import SendMessageRequest

   async def main():
       client = SignalClient()
       ping_command = Command(triggers=["!ping"])

       async def ping_handler(context: Context) -> None:
           response = SendMessageRequest(
               message="Pong! 🏓",
               recipients=[]
           )
           await context.reply(response)

       ping_command.with_handler(ping_handler)
       client.register(ping_command)
       await client.start()

   if __name__ == "__main__":
       asyncio.run(main())
   ```

## Operations

- CI runs linting (`ruff`), format checks (`ruff format --check`), type checks (`mypy`), security scans (`pip-audit`), unit/integration tests (`pytest-safe`), API parity audits (`audit-api`), and `release-guard` on every push.
- `release-guard` keeps publishing blocked until compatibility notes and migrations are confirmed by the reviewer.
