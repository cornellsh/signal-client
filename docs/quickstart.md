# Quickstart

Link a Signal device, send your first message, and verify observability in under 20 minutes.

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

Create a simple bot to test your setup:

/// codexec

    :::python
    from signal_client.bot import SignalClient
    from signal_client.context import Context
    from signal_client.command import Command

    # Initialize the Signal Client
    client = SignalClient()

    # Create a simple command
    hello_command = Command(triggers=["hello", "hi"])

    async def hello_handler(context: Context) -> None:
        """Respond to hello messages."""
        await context.reply("Signal Client is online! 👋")

    # Register the command
    hello_command.with_handler(hello_handler)
    client.register(hello_command)

    if __name__ == "__main__":
        import asyncio
        asyncio.run(client.start())
///

!!! tip "Testing your bot"
    Send "hello" or "hi" to your linked Signal device to test the bot. The bot should respond with "Signal Client is online! 👋"

[=75% "First command registered"]{: .warning}

## Validate your environment

Use the available CLI tools to verify your setup:

- `inspect-dlq` — Inspect the Dead Letter Queue for failed messages
- `release-guard` — Run production readiness checks
- `audit-api` — Audit API endpoints and configurations

!!! info "Available CLI commands"
    The Signal Client provides several CLI utilities for debugging and operations. Run each command without arguments to see available options.

!!! tip "Pin your configuration"
    Commit `signal_client.toml` into version control with secrets removed. Use environment variables or secret stores for sensitive overrides.

[=100% "Ready for automation"]{: .success}

> **Next step** · Deep-dive into runtime structure in [Architecture](architecture.md).

[^persist]: Persisting the volume across container restarts prevents losing the linked device registration.
