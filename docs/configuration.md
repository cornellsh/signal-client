---
title: Configuration
summary: Tune Signal Client for local development and production deployments.
order: 12
---

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `SIGNAL_CLIENT_NUMBER` | _required_ | Linked Signal phone number used for outbound messaging. |
| `SIGNAL_CLIENT_REST_URL` | `http://localhost:8080` | Base URL for the signal-cli REST bridge. |
| `SIGNAL_CLIENT_SECRETS_DIR` | `$HOME/.local/share/signal-api` | Path to credential bundle; mount read-only in production. |
| `SIGNAL_CLIENT_QUEUE_BACKEND` | `sqlite:///./signal_client.db` | Queue/DLQ storage backend URL. |
| `SIGNAL_CLIENT_METRICS_PORT` | `9300` | Port exposing Prometheus metrics. |
| `SIGNAL_CLIENT_RELEASE_GUARD` | `true` | Enforces release checks prior to processing jobs. |

/// caption
Configuration keys consumed by the runtime
///

!!! warning "Never commit secrets"
    Any file within `SIGNAL_CLIENT_SECRETS_DIR` contains your Signal registration keys. Keep the directory out of Git and other artifact stores.

## Mode-specific settings

/// details | CLI development
- Override `SIGNAL_CLIENT_QUEUE_BACKEND=sqlite:///./dev.db` to keep state per project.
- Set `SIGNAL_CLIENT_METRICS_PORT=0` to disable metrics locally when the port conflicts.
- Disable release guard with `SIGNAL_CLIENT_RELEASE_GUARD=false` for faster iteration.
///

/// details | Container deployment
- Pass environment values via Docker Compose or Kubernetes Secrets.
- Mount the credential bundle read-only at `/run/signal/secrets` and set `SIGNAL_CLIENT_SECRETS_DIR` accordingly.
- Configure `SIGNAL_CLIENT_QUEUE_BACKEND=redis://redis:6379/0` for shared state.
///

/// details | Edge / TEE workloads
- Bake secrets into hardware-backed vaults; point `SIGNAL_CLIENT_SECRETS_DIR` to the decrypted mount.
- Set `SIGNAL_CLIENT_QUEUE_BACKEND=sqlite:///./signal_client.db?mode=ro` and forward events to a central DLQ via webhook.
- Use `SIGNAL_CLIENT_METRICS_PORT=127.0.0.1:9300` so only the attested enclave exposes metrics.
///

## Required file structure

```text
signal-client/
├── signal_client.toml
├── secrets/
│   └── registration.yaml
└── storage/
    └── signal_client.db
```

!!! danger "Validate permissions"
    Ensure `registration.yaml` is readable only by the runtime user (`chmod 600`). On container platforms, mount secrets as tmpfs to avoid persisting credentials to disk snapshots.

[Diagnostics playbook](observability.md#alerts-and-dashboards){: class="inline-flex items-center gap-2 rounded-md border border-border px-4 py-2" }
[Operations runbooks](operations.md){: class="inline-flex items-center gap-2 rounded-md border border-border px-4 py-2" }

> **Next step** · Measure how the runtime behaves in [Observability](observability.md).
