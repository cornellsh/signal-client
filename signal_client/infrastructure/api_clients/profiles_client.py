from __future__ import annotations

from typing import Any, cast

import aiohttp


class ProfilesClient:
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

    async def update_profile(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update Profile."""
        response = await self._request("PUT", f"/v1/profiles/{phone_number}", json=data)
        return cast("dict[str, Any]", response)
