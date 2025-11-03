from __future__ import annotations

import asyncio

import structlog

from signal_client.infrastructure.websocket_client import WebSocketClient

log = structlog.get_logger()


class UnsupportedMessageError(Exception):
    """Custom exception for unsupported message types."""


class MessageService:
    def __init__(
        self, websocket_client: WebSocketClient, queue: asyncio.Queue[str]
    ) -> None:
        self._websocket_client = websocket_client
        self._queue = queue

    async def listen(self) -> None:
        """Listen for incoming messages and process them."""
        async for raw_message in self._websocket_client.listen():
            try:
                self._queue.put_nowait(raw_message)
            except asyncio.QueueFull:
                log.warning("Message queue is full, dropping message")
