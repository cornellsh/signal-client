from __future__ import annotations

from typing import Any

import aiohttp


class DevicesClient:
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

    async def get_devices(self, phone_number: str) -> list[dict[str, Any]]:
        """List linked devices."""
        return await self._request("GET", f"/v1/devices/{phone_number}")

    async def add_device(
        self, phone_number: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Links another device to this device."""
        return await self._request("POST", f"/v1/devices/{phone_number}", json=data)

    async def get_qrcodelink(self) -> dict[str, Any]:
        """Link device and generate QR code."""
        return await self._request("GET", "/v1/qrcodelink")

    async def register(self, phone_number: str) -> dict[str, Any]:
        """Register a phone number."""
        return await self._request("POST", f"/v1/register/{phone_number}")

    async def verify(self, phone_number: str, token: str) -> dict[str, Any]:
        """Verify a registered phone number."""
        return await self._request("POST", f"/v1/register/{phone_number}/verify/{token}")

    async def unregister(self, phone_number: str) -> dict[str, Any]:
        """Unregister a phone number."""
        return await self._request("POST", f"/v1/unregister/{phone_number}")