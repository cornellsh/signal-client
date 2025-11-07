---
title: Operations
summary: Runbooks for keeping Signal Client healthy in production.
order: 14
---

## Upgrade checklist

1. `signal-client release-guard --check` — exit code must be zero before deploying.
2. Deploy new containers with rolling strategy; keep at least one worker on the previous version.
3. Monitor `signal_client_latency_seconds` and DLQ counters during rollout.
4. Rotate workers back if latency doubles or DLQ growth exceeds baseline.

!!! note "Plan maintenance windows"
    Signal network limits high-rate device reconnects. Schedule upgrades during low traffic to avoid reconnect storms.

## Incident response

/// details | Bridge connectivity issues
1. Confirm REST bridge container is healthy; restart if unresponsive.
2. Run `signal-client compatibility` to validate the bridge still trusts your link.
3. If the device was unlinked, re-run the [Quickstart](quickstart.md#link-your-signal-device) flow.
///

/// details | Message backlog
1. Inspect the DLQ: `signal-client dlq list --limit 20`.
2. Replay messages once underlying services recover: `signal-client dlq replay --all`.
3. Consider scaling workers temporarily (see below).
///

/// details | Configuration drift
1. Run `signal-client config diff --baseline path/to/baseline.toml`.
2. Reconcile differences, then lock configuration via your secret store.
3. Trigger release guard before re-enabling automation.
///

!!! danger "Pause automation when reprocessing"
    Disable cron jobs and webhook ingestion before replaying the DLQ, otherwise customers may receive duplicate replies.

## Scaling strategy

| Situation | Action |
| --- | --- |
| Gradual volume increase | Increase worker count via `WORKER_CONCURRENCY` or replica count. |
| Short-term surge | Queue jobs in Redis, enable rate limiting per command, drain after peak. |
| Sustained high demand | Shard workloads by Signal number across multiple linked devices. |

> **Next step** · Explore the command API in [API Reference](api-reference.md) or continue with [Guides](guides/writing-async-commands.md).
