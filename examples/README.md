# Examples

Runnable samples that exercise core behaviors with minimal dependencies.

## Prerequisites
- A Signal phone number registered with `signal-cli`.
- A running `signal-cli-rest-api` instance (websocket + REST).
- Environment variables set for the account:
  - `SIGNAL_PHONE_NUMBER`
  - `SIGNAL_SERVICE_URL` (websocket host, e.g., `http://localhost:8080`)
  - `SIGNAL_API_URL` (REST host, e.g., `http://localhost:8080`)

## Run commands
- `poetry run python examples/ping_bot.py` — replies `pong` to `!ping` for quick validation.
- `poetry run python examples/reminder_bot.py` — schedules `!remind <seconds> <message>` reminders and sends them back to the sender.
- `poetry run python examples/webhook_relay.py` — starts an HTTP server and relays POSTed JSON `{recipients, message}` to Signal (`/relay`, port 8081).
