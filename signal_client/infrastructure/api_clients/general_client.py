from __future__ import annotations

from typing import Any, cast

import aiohttp


class GeneralClient:
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

    async def get_about(self) -> dict[str, Any]:
        """Lists general information about the API."""
        response = await self._request("GET", "/v1/about")
        return cast("dict[str, Any]", response)

    async def get_configuration(self) -> dict[str, Any]:
        """List the REST API configuration."""
        response = await self._request("GET", "/v1/configuration")
        return cast("dict[str, Any]", response)

    async def set_configuration(self, data: dict[str, Any]) -> dict[str, Any]:
        """Set the REST API configuration."""
        response = await self._request("POST", "/v1/configuration", json=data)
        return cast("dict[str, Any]", response)

    async def get_settings(self, phone_number: str) -> dict[str, Any]:
        """List account specific settings."""
        response = await self._request(
            "GET", f"/v1/configuration/{phone_number}/settings"
        )
        return cast("dict[str, Any]", response)

    async def set_settings(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Set account specific settings."""
        response = await self._request(
            "POST", f"/v1/configuration/{phone_number}/settings", json=data
        )
        return cast("dict[str, Any]", response)

    async def get_health(self) -> dict[str, Any]:
        """API Health Check."""
        response = await self._request("GET", "/v1/health")
        return cast("dict[str, Any]", response)
