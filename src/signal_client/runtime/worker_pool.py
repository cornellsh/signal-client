from __future__ import annotations

import asyncio
import json
import math
import time
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from zlib import crc32

import structlog

from signal_client.command import Command, CommandError
from signal_client.context import Context
from signal_client.exceptions import UnsupportedMessageError
from signal_client.infrastructure.schemas.message import Message
from signal_client.observability.metrics import (
    ERRORS_OCCURRED,
    MESSAGE_QUEUE_DEPTH,
    MESSAGE_QUEUE_LATENCY,
    MESSAGES_PROCESSED,
)
from signal_client.runtime.command_router import CommandRouter
from signal_client.runtime.models import QueuedMessage
from signal_client.services.checkpoint_store import IngestCheckpointStore
from signal_client.services.dead_letter_queue import DeadLetterQueue
from signal_client.services.lock_manager import LockManager
from signal_client.services.message_parser import MessageParser

log = structlog.get_logger()

MiddlewareCallable = Callable[
    [Context, Callable[[Context], Awaitable[None]]], Awaitable[None]
]


@dataclass(slots=True)
class WorkerConfig:
    context_factory: Callable[[Message], Context]
    queue: asyncio.Queue[QueuedMessage]
    message_parser: MessageParser
    router: CommandRouter
    middleware: Iterable[MiddlewareCallable]
    dead_letter_queue: DeadLetterQueue | None
    checkpoint_store: IngestCheckpointStore | None
    lock_manager: LockManager | None = None
    queue_depth_getter: Callable[[], int] | None = None


class Worker:
    def __init__(
        self, config: WorkerConfig, worker_id: int = 0, shard_id: int = 0
    ) -> None:
        self._context_factory = config.context_factory
        self._queue = config.queue
        self._message_parser = config.message_parser
        self._router = config.router
        self._middleware: list[MiddlewareCallable] = list(config.middleware)
        self._stop = asyncio.Event()
        self._worker_id = worker_id
        self._shard_id = shard_id
        self._dead_letter_queue = config.dead_letter_queue
        self._checkpoint_store = config.checkpoint_store
        self._lock_manager = config.lock_manager
        self._queue_depth_getter = config.queue_depth_getter

    def stop(self) -> None:
        self._stop.set()

    def add_middleware(self, middleware: MiddlewareCallable) -> None:
        self._middleware.append(middleware)

    async def process_messages(self) -> None:
        while not self._stop.is_set():
            try:
                queued_item = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                queued_message = (
                    queued_item
                    if isinstance(queued_item, QueuedMessage)
                    else QueuedMessage(
                        raw=str(queued_item),
                        enqueued_at=time.perf_counter(),
                    )
                )
                latency = time.perf_counter() - queued_message.enqueued_at
                try:
                    MESSAGE_QUEUE_LATENCY.observe(latency)
                    structlog.contextvars.bind_contextvars(
                        worker_id=self._worker_id,
                        shard_id=self._shard_id,
                        queue_depth=self._queue.qsize(),
                    )
                    message = queued_message.message or self._message_parser.parse(
                        queued_message.raw
                    )
                    if message:
                        await self.process(message, latency, queued_message=queued_message)
                        MESSAGES_PROCESSED.inc()
                except UnsupportedMessageError as error:
                    log.debug("worker.unsupported_message", error=error)
                    ERRORS_OCCURRED.inc()
                except (json.JSONDecodeError, KeyError):
                    log.exception(
                        "worker.message_parse_failed",
                        raw_message=queued_message.raw,
                        worker_id=self._worker_id,
                    )
                    await self._send_to_dlq(
                        reason="parse_failed",
                        raw=queued_message.raw,
                        metadata={"worker_id": self._worker_id},
                    )
                    ERRORS_OCCURRED.inc()
                finally:
                    self._queue.task_done()
                    self._acknowledge(queued_message)
                    queue_depth = (
                        self._queue_depth_getter()
                        if self._queue_depth_getter
                        else self._queue.qsize()
                    )
                    MESSAGE_QUEUE_DEPTH.set(queue_depth)
                    structlog.contextvars.clear_contextvars()
            except asyncio.TimeoutError:  # noqa: PERF203
                continue

    async def process(  # compatibility alias for legacy tests/callers
        self,
        message: Message,
        queue_latency: float | None = None,
        *,
        queued_message: QueuedMessage | None = None,
    ) -> None:
        structlog.contextvars.bind_contextvars(
            message_id=message.id,
            source=message.source,
            timestamp=message.timestamp,
        )
        if await self._is_duplicate(message):
            log.debug(
                "worker.duplicate_suppressed",
                message_id=str(message.id),
                source=message.source,
                timestamp=message.timestamp,
            )
            return
        recipient = message.recipient()
        if self._lock_manager and recipient:
            async with self._lock_manager.lock(recipient):
                await self._dispatch_message(
                    message,
                    queue_latency,
                    queued_message=queued_message,
                )
            return

        await self._dispatch_message(
            message,
            queue_latency,
            queued_message=queued_message,
        )

    async def _dispatch_message(
        self,
        message: Message,
        queue_latency: float | None = None,
        *,
        queued_message: QueuedMessage | None = None,
    ) -> None:
        context = self._context_factory(message)
        text = context.message.message
        if not isinstance(text, str) or not text:
            await self._mark_checkpoint(message, queued_message)
            return

        command, trigger = self._router.match(text)
        if command is None or not self._is_whitelisted(command, context):
            await self._mark_checkpoint(message, queued_message)
            return

        handler = getattr(command, "handle", None)
        handler_name = getattr(handler, "__name__", command.__class__.__name__)
        try:
            structlog.contextvars.bind_contextvars(
                command_name=handler_name,
                worker_id=self._worker_id,
                shard_id=self._shard_id,
                queue_latency=queue_latency,
            )
            await self._execute_with_middleware(command, context)
            await self._mark_checkpoint(message, queued_message)
        except Exception:
            log.exception(
                "worker.command_failed",
                command_name=handler_name,
                trigger=trigger,
                worker_id=self._worker_id,
                shard_id=self._shard_id,
                queue_latency=queue_latency,
                message_id=str(message.id),
            )
            await self._send_to_dlq(
                reason="command_failed",
                raw=queued_message.raw if queued_message else None,
                metadata={
                    "command": handler_name,
                    "trigger": trigger,
                    "worker_id": self._worker_id,
                    "shard_id": self._shard_id,
                    "message_id": str(message.id),
                    "source": message.source,
                    "timestamp": message.timestamp,
                },
            )
            ERRORS_OCCURRED.inc()

    @staticmethod
    def _is_whitelisted(command: Command, context: Context) -> bool:
        if not command.whitelisted:
            return True
        return context.message.source in command.whitelisted

    async def _execute_with_middleware(
        self, command: Command, context: Context
    ) -> None:
        if command.handle is None:
            message = "Command handler is not configured."
            raise CommandError(message)

        async def invoke(index: int, ctx: Context) -> None:
            if index >= len(self._middleware):
                await command.handle(ctx)
                return

            middleware_fn = self._middleware[index]

            async def next_callable(next_ctx: Context) -> None:
                await invoke(index + 1, next_ctx)

            await middleware_fn(ctx, next_callable)

        await invoke(0, context)

    async def _mark_checkpoint(
        self, message: Message, queued_message: QueuedMessage | None
    ) -> None:
        if not self._checkpoint_store:
            return
        try:
            await self._checkpoint_store.mark_processed(
                source=message.source,
                timestamp=message.timestamp,
                enqueued_at=queued_message.enqueued_at if queued_message else None,
            )
        except Exception:  # pragma: no cover - defensive
            log.warning(
                "worker.checkpoint_failed",
                source=message.source,
                timestamp=message.timestamp,
            )

    async def _is_duplicate(self, message: Message) -> bool:
        if not self._checkpoint_store:
            return False
        try:
            return await self._checkpoint_store.is_duplicate(
                source=message.source, timestamp=message.timestamp
            )
        except Exception:  # pragma: no cover - defensive
            log.warning(
                "worker.checkpoint_lookup_failed",
                source=message.source,
                timestamp=message.timestamp,
            )
            return False

    async def _send_to_dlq(
        self,
        *,
        reason: str,
        raw: str | None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        if not self._dead_letter_queue or raw is None:
            return
        payload: dict[str, object] = {"raw": raw, "reason": reason}
        if metadata:
            payload["metadata"] = metadata
        try:
            await self._dead_letter_queue.send(payload)
        except Exception:  # pragma: no cover - defensive
            log.warning(
                "worker.dlq_send_failed",
                reason=reason,
                worker_id=self._worker_id,
            )

    def _acknowledge(self, queued_message: QueuedMessage) -> None:
        ack = queued_message.ack
        if ack is None:
            return
        try:
            ack()
        except Exception:  # pragma: no cover - defensive
            log.warning(
                "worker.ack_failed",
                worker_id=self._worker_id,
                shard_id=self._shard_id,
            )


class WorkerPool:
    def __init__(
        self,
        context_factory: Callable[[Message], Context],
        queue: asyncio.Queue[QueuedMessage],
        message_parser: MessageParser,
        *,
        router: CommandRouter | None = None,
        pool_size: int = 4,
        dead_letter_queue: DeadLetterQueue | None = None,
        checkpoint_store: IngestCheckpointStore | None = None,
        shard_count: int | None = None,
        lock_manager: LockManager | None = None,
    ) -> None:
        self._context_factory = context_factory
        self._queue = queue
        self._message_parser = message_parser
        self._router = router or CommandRouter()
        self._pool_size = pool_size
        self._shard_count = shard_count or pool_size
        self._middleware: list[MiddlewareCallable] = []
        self._middleware_ids: set[int] = set()
        self._workers: list[Worker] = []
        self._tasks: list[asyncio.Task[None]] = []
        self._started = asyncio.Event()
        self._dead_letter_queue = dead_letter_queue
        self._checkpoint_store = checkpoint_store
        self._lock_manager = lock_manager
        self._shard_queues: list[asyncio.Queue[QueuedMessage]] = []
        self._distributor_task: asyncio.Task[None] | None = None
        self._distributor_stop = asyncio.Event()

    @property
    def router(self) -> CommandRouter:
        return self._router

    def register(self, command: Command) -> None:
        self._router.register(command)

    def register_middleware(self, middleware: MiddlewareCallable) -> None:
        if id(middleware) in self._middleware_ids:
            return
        self._middleware.append(middleware)
        self._middleware_ids.add(id(middleware))
        for worker in self._workers:
            worker.add_middleware(middleware)

    def start(self) -> None:
        if self._started.is_set():
            return
        if self._shard_count <= 0:
            raise ValueError("shard_count must be positive.")
        if self._pool_size < self._shard_count:
            raise ValueError("worker_pool_size must be >= shard_count.")

        self._initialize_shards()
        self._start_distributor()

        for worker_id in range(self._pool_size):
            shard_id = worker_id % self._shard_count
            worker_config = WorkerConfig(
                context_factory=self._context_factory,
                queue=self._shard_queues[shard_id],
                message_parser=self._message_parser,
                router=self._router,
                middleware=self._middleware,
                dead_letter_queue=self._dead_letter_queue,
                checkpoint_store=self._checkpoint_store,
                lock_manager=self._lock_manager,
                queue_depth_getter=self._queue_depth,
            )
            worker = Worker(
                worker_config,
                worker_id=worker_id,
                shard_id=shard_id,
            )
            self._workers.append(worker)
            task = asyncio.create_task(worker.process_messages())
            self._tasks.append(task)
        self._started.set()

    def stop(self) -> None:
        self._distributor_stop.set()
        for worker in self._workers:
            worker.stop()

    async def join(self) -> None:
        if self._distributor_task:
            await self._distributor_task
        if self._tasks:
            await asyncio.gather(*self._tasks)

    def _initialize_shards(self) -> None:
        if self._shard_queues:
            return
        if self._shard_count <= 0:
            self._shard_count = 1

        per_shard_size = (
            math.ceil(self._queue.maxsize / self._shard_count)
            if self._queue.maxsize > 0
            else 0
        )
        if per_shard_size <= 0 and self._queue.maxsize > 0:
            per_shard_size = 1

        self._shard_queues = [
            asyncio.Queue(maxsize=per_shard_size) for _ in range(self._shard_count)
        ]

    def _start_distributor(self) -> None:
        if self._distributor_task:
            return
        self._distributor_stop.clear()
        self._distributor_task = asyncio.create_task(self._distribute_messages())

    async def _distribute_messages(self) -> None:
        while True:
            if self._distributor_stop.is_set() and self._queue.empty():
                return
            try:
                queued_item = await asyncio.wait_for(self._queue.get(), timeout=1.0)
            except asyncio.TimeoutError:  # noqa: PERF203
                continue

            queued_message = (
                queued_item
                if isinstance(queued_item, QueuedMessage)
                else QueuedMessage(
                    raw=str(queued_item),
                    enqueued_at=time.perf_counter(),
                )
            )
            if queued_message.message is None:
                queued_message.message = self._message_parser.parse(
                    queued_message.raw
                )

            recipient = queued_message.recipient
            if queued_message.message:
                recipient = queued_message.message.recipient()
            elif recipient is None:
                recipient = self._message_parser.recipient_from_raw(
                    queued_message.raw
                )
            queued_message.recipient = recipient

            if queued_message.ack:
                existing_ack = queued_message.ack

                def _combined_ack(existing_ack=existing_ack) -> None:
                    existing_ack()
                    self._queue.task_done()

                queued_message.ack = _combined_ack
            else:
                queued_message.ack = self._queue.task_done

            shard_index = self._compute_shard(recipient)

            try:
                await self._shard_queues[shard_index].put(queued_message)
            except Exception:
                log.exception(
                    "worker_pool.shard_enqueue_failed",
                    shard_id=shard_index,
                )
                try:
                    self._queue.task_done()
                except Exception:  # pragma: no cover - defensive
                    pass
            else:
                self._set_queue_depth_metric()

    def _compute_shard(self, recipient: str | None) -> int:
        if not self._shard_queues:
            return 0
        if not recipient:
            return 0
        shard_index = crc32(recipient.encode("utf-8")) % len(self._shard_queues)
        return shard_index

    def _queue_depth(self) -> int:
        shard_depth = sum(queue.qsize() for queue in self._shard_queues)
        return self._queue.qsize() + shard_depth

    def _set_queue_depth_metric(self) -> None:
        MESSAGE_QUEUE_DEPTH.set(self._queue_depth())


__all__ = [
    "CommandRouter",
    "MiddlewareCallable",
    "Worker",
    "WorkerConfig",
    "WorkerPool",
]
