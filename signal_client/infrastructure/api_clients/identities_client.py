from __future__ import annotations

from typing import Any

import aiohttp


class IdentitiesClient:
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

    async def get_identities(self, phone_number: str) -> list[dict[str, Any]]:
        """List Identities."""
        return await self._request("GET", f"/v1/identities/{phone_number}")

    async def trust_identity(
        self, phone_number: str, number_to_trust: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Trust Identity."""
        return await self._request(
            "PUT", f"/v1/identities/{phone_number}/trust/{number_to_trust}", json=data
        )