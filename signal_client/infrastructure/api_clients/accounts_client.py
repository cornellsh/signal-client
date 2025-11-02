from __future__ import annotations

from typing import Any

import aiohttp


class AccountsClient:
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

    async def get_accounts(self) -> list[dict[str, Any]]:
        """List all accounts."""
        return await self._request("GET", "/v1/accounts")

    async def set_pin(self, phone_number: str, data: dict[str, Any]) -> dict[str, Any]:
        """Set Pin."""
        return await self._request("POST", f"/v1/accounts/{phone_number}/pin", json=data)

    async def remove_pin(self, phone_number: str) -> dict[str, Any]:
        """Remove Pin."""
        return await self._request("DELETE", f"/v1/accounts/{phone_number}/pin")

    async def lift_rate_limit(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Lift rate limit restrictions."""
        return await self._request(
            "POST", f"/v1/accounts/{phone_number}/rate-limit-challenge", json=data
        )

    async def update_settings(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update the account settings."""
        return await self._request(
            "PUT", f"/v1/accounts/{phone_number}/settings", json=data
        )

    async def set_username(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Set a username."""
        return await self._request(
            "POST", f"/v1/accounts/{phone_number}/username", json=data
        )

    async def remove_username(self, phone_number: str) -> dict[str, Any]:
        """Remove a username."""
        return await self._request("DELETE", f"/v1/accounts/{phone_number}/username")