# Architecture

!!! info "Who should read this"
    Use this guide when you want to reason about the runtime internals, model failure modes, or extend Signal Client with new services.

Signal Client is organised into three layers that collaborate to ingest messages, execute commands, and interact with the Signal REST API safely.

```mermaid
graph TD
    A[Signal User] -->|Messages| B[signal-cli-rest-api]
    B -->|JSON-RPC| C[WebSocketClient]
    C --> D[MessageService]
    D --> E[MessageQueue (QueuedMessage)]
    subgraph Worker Pool
        E --> F[Worker]
        F --> G[MessageParser]
        F --> H[Command Execution]
        F --> I[RateLimiter]
        F --> J[CircuitBreaker]
        F --> K[DeadLetterQueue]
    end
    H --> L[Context]
    L --> M[REST API Clients]
    M --> B
```

## 1. Application Layer

### SignalClient

- Bootstraps the dependency-injector container.
- Runs `check_supported_versions()` before loading settings.
- Wires commands and middleware into the worker pool.
- Coordinates startup/shutdown of the message service and worker pool.

### Container

- Provides factories for settings, queues, storage backends, API clients, and services.
- Supports overrides for testing (e.g., fake queues or API clients).

### Context

- Passed to every command execution.
- Exposes `message`, the original `QueuedMessage`, typed API clients, shared locks, rate limiter/circuit breaker helpers, and structured logging context.

## 2. Core Services

### MessageService

- Listens for incoming JSON-RPC events via `WebSocketClient`.
- Wraps payloads in `QueuedMessage` capturing `enqueued_at` timestamps.
- Attempts to enqueue with a timeout; optionally drops the oldest message when the queue is full.
- Updates the `message_queue_depth` gauge after each enqueue attempt.

### WorkerPoolManager & Worker

- Spawns a bounded set of workers (configured via `worker_pool_size`).
- Compiles string and regex triggers, registers middleware, and binds structlog context for each message.
- Workers parse payloads into `Message` schemas and invoke the matching command.
- Records queue latency in the `message_queue_latency_seconds` histogram and increments `messages_processed_total` / `errors_occurred_total` counters.

### MessageParser

- Converts raw JSON into strongly typed Pydantic models (`Message`, `Contact`, `Group`, etc.).
- Validates required fields and normalises attachments, quotes, and reactions for downstream use.

### RateLimiter & CircuitBreaker

- Rate limiter enforces API quotas and records wait time via the `rate_limiter_wait_seconds` histogram.
- Circuit breaker wraps outbound API invocations, exposing `circuit_breaker_state` metrics and preventing cascading failures.

### DeadLetterQueue

- Persists failed messages in the configured storage backend with retry metadata.
- Tracks backlog via the `dead_letter_queue_depth` gauge and exposes `inspect()` / `replay()` helpers for maintenance tooling.

## 3. Infrastructure Layer

### WebSocketClient

- Maintains the persistent websocket connection to `signal-cli-rest-api`.
- Handles reconnect loops and exposes health logging.

### BaseClient & REST Clients

- `BaseClient` shares aiohttp sessions, authentication, structured error handling, and retry-friendly exceptions.
- Vertically sliced clients live in `infrastructure/api_clients/` (e.g., `messages_client`, `groups_client`).
- Each client mirrors a resource in the REST API and reuses shared schemas.

### Schemas (`infrastructure/schemas`)

- Pydantic models representing requests/responses for all API surfaces.
- Shared by parser, context, and service layers to ensure type safety.

### Storage Adapters (`infrastructure/storage`)

- Optional Redis/SQLite implementations for DLQ persistence or custom extensions.
- Controlled via settings; tests cover compatibility and fallback behaviour.

## 4. Execution Flow

1. `SignalClient.start()` launches `MessageService.listen()` and `WorkerPoolManager.join()`.
2. Incoming Signal events are queued as `QueuedMessage` instances with timestamps.
3. Workers pull messages, calculate queue latency, and select commands matching compiled triggers.
4. Commands execute inside middleware pipeline, using `Context` to interact with REST clients, rate limiter, and circuit breaker.
5. Errors propagate to DLQ with structured metadata; operators can replay once dependencies recover.

## 5. Extensibility Hooks

- **Commands:** implement the `Command` protocol; add optional `before_handle`/`after_handle` hooks.
- **Middleware:** functions receiving `(context, call_next)`; register via `SignalClient.use()`.
- **Container overrides:** provide custom implementations (e.g., swapping storage provider) by overriding providers before `SignalClient` instantiation.
- **Metrics:** use `prometheus_client` directly or call `signal_client.metrics.render_metrics()` when embedding the exposition endpoint.

For more operational context, continue to [Observability](./observability.md) and [Operations](./operations.md).

---

**Next up:** Tune runtime settings in [Configuration](./configuration.md) and instrument your deployment via [Observability](./observability.md).
