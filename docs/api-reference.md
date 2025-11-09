# API Reference

Programmatic surfaces for extending Signal Client.

## Core Classes

### SignalClient

::: signal_client.bot.SignalClient
    options:
        members: true
        heading_level: 4
        docstring_section_style: table

### Context

::: signal_client.context.Context
    options:
        members: true
        heading_level: 4
        docstring_section_style: table

!!! info "Import paths"
    All public APIs live under `signal_client`. Import them directly:
    
    ```python
    from signal_client.bot import SignalClient
    from signal_client.context import Context
    from signal_client.command import Command
    ```

## CLI Tools

The Signal Client provides several command-line utilities:

| Command | Description |
| --- | --- |
| `inspect-dlq` | Inspect the contents of the Dead Letter Queue |
| `release-guard` | Run production-readiness checks before deployment |
| `audit-api` | Audit API endpoints and configurations |
| `pytest-safe` | Run tests with proper cleanup for async resources |

!!! tip "Getting help"
    Run any CLI command without arguments to see available options and usage information.

## REST hooks

```json
{
  "event": "message.received",
  "message": {
    "source": "+19998887777",
    "timestamp": 1730931090,
    "text": "Hello bot",
    "attachments": []
  }
}
```

> **Next step** · Extend the runtime with your own commands in [Guides](guides/writing-async-commands.md).
