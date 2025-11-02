from __future__ import annotations

from typing import Any, cast

import aiohttp


class DevicesClient:
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

    async def get_devices(self, phone_number: str) -> list[dict[str, Any]]:
        """List linked devices."""
        response = await self._request("GET", f"/v1/devices/{phone_number}")
        return cast("list[dict[str, Any]]", response)

    async def add_device(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Links another device to this device."""
        response = await self._request("POST", f"/v1/devices/{phone_number}", json=data)
        return cast("dict[str, Any]", response)

    async def get_qrcodelink(self) -> dict[str, Any]:
        """Link device and generate QR code."""
        response = await self._request("GET", "/v1/qrcodelink")
        return cast("dict[str, Any]", response)

    async def register(self, phone_number: str) -> dict[str, Any]:
        """Register a phone number."""
        response = await self._request("POST", f"/v1/register/{phone_number}")
        return cast("dict[str, Any]", response)

    async def verify(self, phone_number: str, token: str) -> dict[str, Any]:
        """Verify a registered phone number."""
        response = await self._request(
            "POST", f"/v1/register/{phone_number}/verify/{token}"
        )
        return cast("dict[str, Any]", response)

    async def unregister(self, phone_number: str) -> dict[str, Any]:
        """Unregister a phone number."""
        response = await self._request("POST", f"/v1/unregister/{phone_number}")
        return cast("dict[str, Any]", response)
