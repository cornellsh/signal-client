---
title: Diagnostics & Troubleshooting
summary: Resolve issues quickly with repeatable checks and safe recovery steps.
order: 16
---

## Common error codes

| Error | Meaning | Fix |
| --- | --- | --- |
| `E-LINK-401` | Device link lost or revoked. | Re-run the linking flow and restart the REST bridge. |
| `E-BRIDGE-504` | REST bridge timed out. | Check Docker logs, ensure network access to Signal, restart container. |
| `E-CMD-429` | Command rate limit exceeded. | Reduce batch size or enable rate limiter middleware. |
| `E-STORAGE-503` | Storage backend unreachable. | Verify Redis/SQLite connectivity and credentials. |

/// caption
Most frequent operational error codes
///

## FAQ

/// details | Why are messages stuck in the DLQ?
- Inspect the DLQ entry: `signal-client dlq describe <id>`.
- Fix the underlying dependency (API, database) and replay jobs.
- If replays continue failing, add guards to the command and deploy before replaying.
///

/// details | How do I verify the REST bridge?
- Call `/v1/health` on the bridge endpoint.
- Run `signal-client compatibility --verbose` and confirm transport checks pass.
- Ensure ports 8080/8081 are accessible from the worker container.[^platform]
///

/// details | What if attachments fail to upload?
- Check disk space on the bridge host.
- Re-upload via `signal-client attachments upload --retry`.
- Confirm the attachment handle is stored before reuse.
///

## Diagnostic commands

```bash
signal-client diagnostics summary
signal-client diagnostics rest-bridge --open
signal-client diagnostics metrics --check-latency
```

!!! danger "Do not clear the DLQ blindly"
    Clearing the DLQ without replaying loses customer messages permanently. Always replay or export entries before purging.

[^platform]: On managed platforms, request firewall updates if the REST bridge cannot reach Signal endpoints.

> **Need more help?** Open a discussion or issue from the [Resources & Community](resources.md) page.
