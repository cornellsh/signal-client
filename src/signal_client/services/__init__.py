from .worker_pool_manager import (
    CommandRouter,
    MiddlewareCallable,
    Worker,
    WorkerConfig,
    WorkerPool,
    WorkerPoolManager,
)

__all__ = [
    "BackpressurePolicy",
    "CommandRouter",
    "MessageService",
    "MiddlewareCallable",
    "Worker",
    "WorkerConfig",
    "WorkerPool",
    "WorkerPoolManager",
]


def __getattr__(name: str):
    if name in {"BackpressurePolicy", "MessageService"}:
        from signal_client.runtime.listener import BackpressurePolicy, MessageService

        return BackpressurePolicy if name == "BackpressurePolicy" else MessageService
    raise AttributeError(name)
