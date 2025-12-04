# Examples

Runnable samples live in `examples/` and assume your environment is configured (see [Getting started](getting_started.md)).

## Ping bot
- File: `examples/ping_bot.py`
- Behavior: replies `pong` to `!ping`.
- Run: `poetry run python examples/ping_bot.py`

## Reminder bot
- File: `examples/reminder_bot.py`
- Behavior: schedules `!remind <seconds> <message>` and sends the reminder back to the sender.
- Run: `poetry run python examples/reminder_bot.py`

## Webhook relay
- File: `examples/webhook_relay.py`
- Behavior: starts an HTTP server (port 8081) that relays POSTed JSON `{recipients, message}` to Signal. Defaults to sending to the configured bot number if recipients are omitted.
- Run: `poetry run python examples/webhook_relay.py`, then POST to `http://localhost:8081/relay`.

All samples expect a running `signal-cli-rest-api` instance reachable at `SIGNAL_SERVICE_URL`/`SIGNAL_API_URL`.
