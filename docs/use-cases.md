# Use Cases

!!! info "Who should read this"
    Look through these examples when you need ideas for Signal bots or want to see how the runtime fits different workflows.

Signal Client handles command routing, retries, and observability so you can focus on the behavior of your bot. The scenarios below are starting points—extend them to match your own groups.

## Moderation helpers

- **Goal:** Keep busy chats tidy by filtering spam, enforcing simple rules, and notifying admins when needed.
- **Runtime support:** Middleware checks message content before commands fire, worker queues throttle follow-up actions, and logs record every decision for later review.
- **Docs to explore:** [Configuration](./configuration.md) · [Operations](./operations.md)

## Alert and status feeds

- **Goal:** Post build notifications, monitoring alerts, or status updates straight into Signal groups.
- **Runtime support:** Worker pools call external APIs without blocking the main loop, retries reschedule failed sends, and metrics highlight latency spikes.
- **Docs to explore:** [Observability](./observability.md) · [Feature Tour](./feature-tour.md)

## Utility commands

- **Goal:** Offer quick commands such as `!help`, `!schedule`, or `!lookup` inside chats.
- **Runtime support:** Typed contexts expose sender details, attachments, and reply helpers; command registration keeps trigger matching simple.
- **Docs to explore:** [Quickstart](./quickstart.md) · [Guides: Writing Async Commands](./guides/writing-async-commands.md)

## Assistants and automation flows

- **Goal:** Build bots that summarize conversations, remind teams about follow-ups, or hand off work to other systems.
- **Runtime support:** Background jobs poll external services, compatibility checks guard upgrades, and dead-letter queues preserve events that need manual review.
- **Docs to explore:** [Architecture](./architecture.md) · [API Reference](./api-reference.md)

## Your turn

- Combine these building blocks with your own ideas. Start with the [API Reference](./api-reference.md) for class details.
- Share finished bots or feature requests in the project discussions.
