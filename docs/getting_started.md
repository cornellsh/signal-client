# Getting Started

Build a minimal Signal bot with the async `signal-client` runtime.

## Prerequisites

- A Signal phone number registered with `signal-cli`.
- A running [`bbernhard/signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api)
  instance (websocket + REST). The defaults assume it listens on
  `http://localhost:8080`.
- Environment exported for your bot:

  ```bash
  export SIGNAL_PHONE_NUMBER=+15551234567
  export SIGNAL_SERVICE_URL=http://localhost:8080   # websocket host
  export SIGNAL_API_URL=http://localhost:8080       # REST host
  ```

## Install

- PyPI: `pip install signal-client`
- Poetry: `poetry add signal_client`
- From source: `poetry install`

## Run your first bot

Create `ping_bot.py` (or use `examples/ping_bot.py`):

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

Then run:

```bash
poetry run python examples/ping_bot.py
```

Send `!ping` from a contact or group that the configured number can reach; the
bot replies with `pong`.

## Next steps

- Try the [reminder](examples.md#reminder-bot) and
  [webhook relay](examples.md#webhook-relay) samples.
- Review [advanced usage](guides/advanced_usage.md) for middleware, attachments,
  and reactions.
- See [operations](guides/production_deployment.md) for storage, DLQ, and
  observability options.
