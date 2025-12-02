from __future__ import annotations

"""Compatibility layer forwarding to the runtime worker pool."""

from signal_client.runtime.worker_pool import (
    CommandRouter,
    MiddlewareCallable,
    Worker,
    WorkerConfig,
    WorkerPool,
)

WorkerPoolManager = WorkerPool

__all__ = [
    "CommandRouter",
    "MiddlewareCallable",
    "Worker",
    "WorkerConfig",
    "WorkerPool",
    "WorkerPoolManager",
]
