---
title: Changelog & Roadmap
summary: Track what shipped and what is coming next for Signal Client.
order: 902
show_datetime: true
---

## Latest releases

- +heroicons:sparkles+ **0.9.0** — Added async command middleware, compatibility guard, and recipes docs.
- +heroicons:wrench-screwdriver+ **0.8.0** — Introduced release guard CLI and Prometheus instrumentation.
- +heroicons:shield-check+ **0.7.0** — Hardened credential storage defaults and added DLQ replay safeguards.

## Roadmap[^timeline]

[=60% "v1.0 readiness"]{: .warning}

| Milestone | Status | Notes |
| --- | --- | --- |
| Story publishing API stabilised | In progress | Waiting on upstream signal-cli changes. |
| Redis queue backend GA | Done | Available since 0.9.0. |
| Multi-device orchestration | Planned | Design review scheduled next quarter. |

/// details | Deprecations
- Legacy environment variable `SIGNAL_CLIENT_BRIDGE_URL` will be removed in v1.0. Use `SIGNAL_CLIENT_REST_URL`.
- The experimental `signal-client stories` CLI subcommand will emit warnings until the API stabilises.
///

[^timeline]: Roadmap dates are target estimates; scope may shift with upstream Signal changes.

> **Want to influence the roadmap?** Vote or comment on proposals in [GitHub discussions](https://github.com/cornellsh/signal-client/discussions).
