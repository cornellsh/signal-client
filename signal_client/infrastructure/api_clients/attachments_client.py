from __future__ import annotations

from typing import Any, cast

import aiohttp


class AttachmentsClient:
    def __init__(self, session: aiohttp.ClientSession, base_url: str) -> None:
        self._session = session
        self._base_url = base_url

    async def _handle_response(
        self, response: aiohttp.ClientResponse
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        response.raise_for_status()
        if response.content_type == "application/json":
            return await response.json()
        return await response.read()

    async def _request(
        self, method: str, path: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        url = f"{self._base_url}{path}"
        async with self._session.request(method, url, **kwargs) as response:
            return await self._handle_response(response)

    async def get_attachments(self) -> list[dict[str, Any]]:
        """List all attachments."""
        response = await self._request("GET", "/v1/attachments")
        return cast("list[dict[str, Any]]", response)

    async def get_attachment(self, attachment_id: str) -> bytes:
        """Serve Attachment."""
        response = await self._request("GET", f"/v1/attachments/{attachment_id}")
        return cast("bytes", response)

    async def remove_attachment(self, attachment_id: str) -> dict[str, Any]:
        """Remove attachment."""
        response = await self._request("DELETE", f"/v1/attachments/{attachment_id}")
        return cast("dict[str, Any]", response)
