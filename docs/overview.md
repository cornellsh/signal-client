---
title: Overview
summary: Understand how Signal Client layers opinionated tooling on top of signal-cli.
order: 1
---

## What you get on day one

- +heroicons:sparkles+ Batteries-included SDK around [`signal-cli-rest-api`](https://github.com/bbernhard/signal-cli-rest-api).
- +heroicons:cog-6-tooth+ Async command runtime with typed contexts and dependency injection helpers.
- +heroicons:signal+ Observability, release guardrails, and production checklists suitable for regulated teams.

!!! note "Mind the prerequisites"
    Signal Client expects a linked Signal device, outbound internet access to Signal's messaging network, and Python {{ signal.min_python }} or newer. Review the [Quickstart](quickstart.md) to confirm your environment before exploring deeper guides.

## Architecture at a glance

| Layer | Responsibilities | Tech highlights |
| --- | --- | --- |
| Interface | CLI, Typer commands, HTTP hooks | Structured logging, compatibility guard |
| Runtime | Command scheduler, worker pools, retry orchestration | APScheduler, asyncio tasks |
| Platform | State stores, queue buffers, observability pipeline | SQLite, Redis (optional), Prometheus |
| Edge | Device link, REST bridge, binary execution | `signal-cli-rest-api`, GraalVM native binary |

/// details | How the runtime flows
1. Messages arrive via the Signal REST bridge (webhook or polling).
2. Container workers deserialize payloads into structured entities and hand them to registered commands.
3. Commands execute with strongly-typed context, emit telemetry, and schedule follow-up work if required.
4. Results are persisted or forwarded through the operations pipeline for auditing.
///

## Quick facts

{{ read_csv("quick-facts.csv") }}

> **Next step** · Pick a use case in [Use Cases](use-cases.md) or skip ahead to implementation in [Quickstart](quickstart.md).
