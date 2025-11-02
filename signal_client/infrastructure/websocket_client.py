from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Callable

import websockets


class WebSocketClient:
    def __init__(
        self,
        signal_service_url: str,
        phone_number: str,
    ):
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
                    async for raw_message in websocket:
                        if not isinstance(raw_message, str):
                            raw_message = bytes(raw_message).decode("utf-8")
                        yield raw_message
            except websockets.exceptions.ConnectionClosed:
                await asyncio.sleep(1)  # Reconnect delay