---
title: API Reference
summary: Programmatic surfaces for extending Signal Client.
order: 15
show_datetime: true
---

## Command runtime

::: signal_client.bot.SignalClient
    options:
        members: true
        heading_level: 3
        docstring_section_style: table
:::

::: signal_client.context.Context
    options:
        members: false
        heading_level: 3
:::

!!! info "Import path"
    All public APIs live under `signal_client`. Reference them directly: `from signal_client.bot import SignalClient`.

## CLI

| Command | Description |
| --- | --- |
| `signal-client send` | Send an outbound message, story, or attachment. |
| `signal-client compatibility` | Verify the local environment and linked device health. |
| `signal-client dlq` | Inspect or replay jobs in the dead-letter queue. |
| `signal-client release-guard` | Run production-readiness checks before enabling workers. |

!!! warning "Preview endpoints"
    The `signal-client stories` subcommand is experimental. Expect breaking changes before v1.0.

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
