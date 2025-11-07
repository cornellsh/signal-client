---
title: Quickstart
summary: Link a Signal device, send your first message, and verify observability in under 20 minutes.
order: 10
---

!!! note "Before you begin"
    - Primary Signal device in hand with permission to link new clients.
    - Python {{ signal.min_python }} or newer, Git, and Docker installed.
    - Outbound internet access to Signal's infrastructure.

## Install the toolkit

/// tab | `pip`

    :::bash
    python -m venv .venv
    source .venv/bin/activate
    pip install signal-client
///

/// tab | `uv`

    :::bash
    uv venv
    source .venv/bin/activate
    uv add signal-client
///

/// tab | `poetry`

    :::bash
    poetry init --name signal-runner --dependency signal-client
    poetry install
///

/// tab | `pipx`

    :::bash
    pipx install signal-client
///

[=20% "Environment provisioned"]

## Link your Signal device

1. Launch the REST API bridge (Docker example below).
   ```bash
   docker run --rm -p 8080:8080 \
     -v "$HOME/.local/share/signal-api:/home/.local/share/signal-cli" \
     -e MODE=native bbernhard/signal-cli-rest-api
   ```
2. Open <http://localhost:8080/v1/qrcodelink?device_name=signal-client> and scan the QR code from *Linked devices* in the Signal mobile app.
3. Export your credentials to the Signal Client configuration directory.[^persist]

!!! warning "Secure the credential bundle"
    The Docker volume contains encryption keys for your Signal identity. Store it on encrypted disk volumes and restrict file permissions before running in production.

[=50% "Device linked"]{: .success}

## Send a test message

Set `SIGNAL_CLIENT_NUMBER` to the linked device number and run:

```bash
signal-client send \
  --recipient "+19998887777" \
  --message "Test message from Signal Client"
```

Verify the message arrives on the target device. If not, restart the container and re-run `receive` via the REST API.

/// codexec

    :::python
    from signal_client.bot import Bot
    from signal_client.command import CommandContext

    bot = Bot(number="+19998887777")

    @bot.command()
    async def hello(context: CommandContext) -> None:
        await context.reply("Signal Client is online!")

    if __name__ == "__main__":
        bot.run()
///

[=75% "First command registered"]{: .warning}

## Validate your environment

- `signal-client compatibility` — checks locale, Java, and signal-cli versions.
- `signal-client release-guard` — dry-run release guard to ensure config is production safe.
- `signal-client metrics` — exposes Prometheus endpoint so you can view counters.

!!! tip "Pin your configuration"
    Commit `signal_client.toml` into version control with secrets removed. Use environment variables or secret stores for sensitive overrides.

[=100% "Ready for automation"]{: .success}

> **Next step** · Deep-dive into runtime structure in [Architecture](architecture.md).

[^persist]: Persisting the volume across container restarts prevents losing the linked device registration.
