from __future__ import annotations

from typing import Any

import aiohttp


class StickerPacksClient:
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

    async def get_sticker_packs(self, phone_number: str) -> list[dict[str, Any]]:
        """List Installed Sticker Packs."""
        return await self._request("GET", f"/v1/sticker-packs/{phone_number}")

    async def add_sticker_pack(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Add Sticker Pack."""
        return await self._request(
            "POST", f"/v1/sticker-packs/{phone_number}", json=data
        )