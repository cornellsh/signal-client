from __future__ import annotations

from typing import Any, cast

import aiohttp


class AccountsClient:
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

    async def get_accounts(self) -> list[dict[str, Any]]:
        """List all accounts."""
        response = await self._request("GET", "/v1/accounts")
        return cast("list[dict[str, Any]]", response)

    async def set_pin(self, phone_number: str, data: dict[str, Any]) -> dict[str, Any]:
        """Set Pin."""
        response = await self._request(
            "POST", f"/v1/accounts/{phone_number}/pin", json=data
        )
        return cast("dict[str, Any]", response)

    async def remove_pin(self, phone_number: str) -> dict[str, Any]:
        """Remove Pin."""
        response = await self._request("DELETE", f"/v1/accounts/{phone_number}/pin")
        return cast("dict[str, Any]", response)

    async def lift_rate_limit(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Lift rate limit restrictions."""
        response = await self._request(
            "POST", f"/v1/accounts/{phone_number}/rate-limit-challenge", json=data
        )
        return cast("dict[str, Any]", response)

    async def update_settings(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update the account settings."""
        response = await self._request(
            "PUT", f"/v1/accounts/{phone_number}/settings", json=data
        )
        return cast("dict[str, Any]", response)

    async def set_username(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Set a username."""
        response = await self._request(
            "POST", f"/v1/accounts/{phone_number}/username", json=data
        )
        return cast("dict[str, Any]", response)

    async def remove_username(self, phone_number: str) -> dict[str, Any]:
        """Remove a username."""
        response = await self._request(
            "DELETE", f"/v1/accounts/{phone_number}/username"
        )
        return cast("dict[str, Any]", response)
