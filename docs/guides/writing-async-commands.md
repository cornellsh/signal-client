---
title: Writing Async Commands
summary: Register, test, and deploy custom Signal Client commands.
order: 200
---

## Scaffold a command

```bash
signal-client scaffold command --name greet
```

This generates `commands/greet.py` with a ready-to-run async function.

/// tab | Python

    :::python
    from signal_client.command import CommandContext

    async def greet(context: CommandContext) -> None:
        await context.reply("Hey there! 👋")
///

/// tab | TypeScript (REST caller)

    :::typescript
    import fetch from "node-fetch";

    await fetch("http://localhost:8080/v2/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: "Hey there! 👋",
        recipients: ["+19998887777"],
        number: process.env.SIGNAL_NUMBER,
      }),
    });
///

## Register it with the bot

```python
from signal_client.bot import Bot
from commands.greet import greet

bot = Bot(number="+19998887777")
bot.command()(greet)

if __name__ == "__main__":
    bot.run()
```

!!! tip "Use dependency injection"

## Core workflows

### Messaging

1. Inspect `context.message` to understand sender, group, and attachments.
2. Compose a reply with `context.reply`, `context.send_attachment`, or `context.reaction`.
3. Record success metrics and exit early on duplicate message IDs.

/// tab | Python

    :::python
    async def ticket_ack(context: CommandContext) -> None:
        await context.reply(
            f"Ticket {context.message.metadata.ticket_id} acknowledged ✅"
        )
        context.metrics.counter("ticket_ack").inc()
///

/// tab | TypeScript (REST caller)

    :::typescript
    await fetch("http://localhost:8080/v2/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: `Ticket ${payload.ticketId} acknowledged ✅`,
        recipients: [payload.sender],
        number: process.env.SIGNAL_NUMBER,
      }),
    });
///

/// codexec

    :::python
    print("Sample Signal Client command registered")
///

### Group management

- +heroicons:user-group+ Create or update groups through the REST bridge (`/v1/groups`) before inviting the runtime bot.
- Maintain a registry of group IDs in SQLite or Redis for quick lookups.
- Use commands to add or remove members by emitting REST calls via an injected service.

```python
await context.groups.add_member(group_id="support-escalation", number="+44123456789")
```

### Media and attachments

1. Upload large files through the REST bridge and capture the returned attachment handle.
2. Reference the handle when sending via `context.send_attachment`.
3. Store handles in persistent storage if you need to reuse them later.

```python
handle = await context.attachments.upload(path="reports/outage.pdf")
await context.send_attachment(handle=handle, caption="Outage summary")
```

### Webhooks and external triggers

- Expose a FastAPI or Flask endpoint that forwards payloads to `Bot.enqueue()`.
- Validate signatures and rate limit external callers to protect worker capacity.
- Enrich the payload with correlation IDs before handing off to the runtime.

```python
@app.post("/hooks/status")
async def status_hook(payload: StatusEvent) -> None:
    await bot.enqueue("status_update", payload.dict(), trace_id=payload.trace_id)
```
    Accept a `CommandContext` argument and resolve services via `context.services.resolve(MyService)` to keep commands easy to test.

## Test locally

1. Start the REST bridge (see [Quickstart](../quickstart.md)).
2. Run `signal-client bot --reload` to enable autoreload while editing your command.
3. Send yourself a test message and confirm the command replies as expected.

[=50% "Command verified"]{: .warning}

## Harden before production

- Add idempotency by checking `context.message.id` against Redis or SQLite.
- Emit metrics with `context.metrics.counter("greet_calls").inc()`.
- Guard against abuse: validate message length and rate limit per sender.

!!! warning "Watch your exception handlers"
    Swallowing exceptions hides DLQ-worthy issues. Allow them to propagate so the runtime retries or escalates appropriately.

[=100% "Production ready"]{: .success}

> **Next step** · Document and export your command interface in [API Reference](../api-reference.md).
