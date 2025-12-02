# Signal Client

[![CI](https://github.com/cornellsh/signal-client/actions/workflows/ci.yml/badge.svg)](https://github.com/cornellsh/signal-client/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/signal-client.svg)](https://pypi.org/project/signal-client/)
[![License](https://img.shields.io/pypi/l/signal_client.svg)](https://github.com/cornellsh/signal_client/blob/main/LICENSE)

**Signal Client is a Python runtime for building Signal bots.** It wraps [`signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api) and gives you typed commands, background workers, retries, and observability in one package.

- `pip install signal-client`
- Command and observability patterns live in `tests/`, so read the scenarios you care about straight from the suite.

## What you get

- Register commands that react to messages in chats and groups.
- Send replies with attachments, mentions, and templated content.
- Run middleware before or after each command to check auth or feature flags.
- Schedule background jobs for reminders, clean-up tasks, or API polling.
- Keep bots healthy with worker pools, retries, and dead-letter queues.
- Export metrics and structured logs for dashboards and alerting.

## Quickstart in three steps

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

The `tests/` directory doubles as living documentation for more advanced flows and background workers.

## Capabilities that matter day to day

- **Typed command context** keeps message bodies, attachments, sender info, and reply helpers in one object.
- **Worker pools, queues, and retries** prevent slow commands from stalling the rest of your bot.
- **Middleware hooks** add authentication, rate limits, keyword filters, or analytics without touching handlers.
- **Scheduled and background work** lets you poll APIs, post reminders, or clean up state on an interval.
- **Structured metrics and logs** give visibility into throughput, failures, and retry loops.
- **Compatibility guards** block unsupported dependency versions before your bot boots.

## Operations

- CI runs linting (`ruff`), format checks (`ruff format --check`), type checks (`mypy`), security scans (`pip-audit`), unit/integration tests (`pytest-safe`), API parity audits (`audit-api`), and `release-guard` on every push.
- `release-guard` keeps publishing blocked until compatibility notes and migrations are confirmed by the reviewer.

### Releases

1. Update `pyproject.toml` to the new version, describe the highlights in the PR, and keep the changelog aligned.
2. Run the CI quality gates (`ruff`, `ruff format --check`, `mypy`, `pytest-safe`, and `pip-audit`) plus `poetry run release-guard` to ensure compatibility before publishing.
3. Execute `python -m semantic_release publish` (with the required PyPI/GitHub credentials) to ship the new artifacts and release notes.

## Support

- Ask questions or request features via [Discussions](https://github.com/cornellsh/signal-client/discussions) or [Issues](https://github.com/cornellsh/signal-client/issues).
- The compatibility command (`python -m signal_client.compatibility --strict`) is your first gate for new environments.

Maintained by [@cornellsh](https://github.com/cornellsh). Feel free to open a discussion if Signal Client powers something helpful.
