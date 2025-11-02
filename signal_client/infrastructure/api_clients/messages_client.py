from __future__ import annotations

from typing import Any

import aiohttp


class MessagesClient:
    def __init__(self, session: aiohttp.ClientSession, base_url: str):
        self._session = session
        self._base_url = base_url

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Any:
        response.raise_for_status()
        if response.content_type == "application/json":
            return await response.json()
        return await response.read()

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self._base_url}{path}"
        async with self._session.request(method, url, **kwargs) as response:
            return await self._handle_response(response)

    async def send(self, data: dict[str, Any]) -> dict[str, Any]:
        """Send a signal message."""
        return await self._request("POST", "/v2/send", json=data)

    async def remote_delete(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Delete a signal message."""
        return await self._request(
            "DELETE", f"/v1/remote-delete/{phone_number}", json=data
        )

    async def set_typing_indicator(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Show Typing Indicator."""
        return await self._request(
            "PUT", f"/v1/typing-indicator/{phone_number}", json=data
        )

    async def unset_typing_indicator(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Hide Typing Indicator."""
        return await self._request(
            "DELETE", f"/v1/typing-indicator/{phone_number}", json=data
        )