from __future__ import annotations

from typing import Any

import aiohttp


class AttachmentsClient:
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

    async def get_attachments(self) -> list[dict[str, Any]]:
        """List all attachments."""
        return await self._request("GET", "/v1/attachments")

    async def get_attachment(self, attachment_id: str) -> bytes:
        """Serve Attachment."""
        return await self._request("GET", f"/v1/attachments/{attachment_id}")

    async def remove_attachment(self, attachment_id: str) -> dict[str, Any]:
        """Remove attachment."""
        return await self._request("DELETE", f"/v1/attachments/{attachment_id}")