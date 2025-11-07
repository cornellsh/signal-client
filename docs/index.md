# Signal Client Docs

> Build Signal bots with typed commands, worker pools, and observability baked in.

[Start with your first command](quickstart.md){ .md-button .md-button--primary }
[Tour the runtime](feature-tour.md){ .md-button }

## Browse the docs

### Overview material

- [Overview](overview.md) — project goals and the high-level architecture.
- [Use Cases](use-cases.md) — examples of bots for moderation, alerts, assistants, and utilities.
- [Feature Tour](feature-tour.md) — how commands, middleware, and services fit together.

### Build a bot

1. [Quickstart](quickstart.md) — pair `signal-cli-rest-api`, install the client, and send a reply.
2. [Configuration](configuration.md) — pick concurrency limits, retries, and storage options.
3. [Architecture](architecture.md) — understand the worker pipeline and message flow.
4. [Observability](observability.md) — add metrics, logs, and compatibility checks.
5. [Operations](operations.md) — runbooks for deployment, DLQ replay, and upgrades.
6. [API Reference](api-reference.md) — full Python surface area.

### Helpful extras

- [Writing Async Commands](guides/writing-async-commands.md) — patterns for non-blocking handlers.
- [Coding Standards](coding_standards.md) — project conventions.
- [Production Secrets](production_secrets.md) — secure credential handling tips.

!!! tip "Stay in the loop"
    Watch the [GitHub repository](https://github.com/cornellsh/signal-client) for release notes and roadmap discussions.

Questions or feedback? Open a discussion or drop an issue.
