from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator

import websockets


class WebSocketClient:
    def __init__(
        self,
        signal_service_url: str,
        phone_number: str,
    ) -> None:
        self._signal_service_url = signal_service_url
        self._phone_number = phone_number
        self._ws_uri = (
            f"ws://{self._signal_service_url}/v1/receive/{self._phone_number}"
        )

    async def listen(self) -> AsyncGenerator[str, None]:
        """Listen for incoming messages and yield them."""
        while True:
            try:
                async with websockets.connect(self._ws_uri) as websocket:
                    async for message in websocket:
                        if isinstance(message, bytes):
                            yield message.decode("utf-8")
                        else:
                            yield message
            except websockets.exceptions.ConnectionClosed:  # noqa: PERF203
                await asyncio.sleep(1)  # Reconnect delay
