from __future__ import annotations

from typing import TYPE_CHECKING, Any

import aiohttp

if TYPE_CHECKING:
    from ...domain.groups import (
        ChangeGroupAdminsRequest,
        ChangeGroupMembersRequest,
        CreateGroupRequest,
        UpdateGroupRequest,
    )


class GroupsClient:
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

    async def get_groups(self, phone_number: str) -> list[dict[str, Any]]:
        """List all Signal Groups."""
        return await self._request("GET", f"/v1/groups/{phone_number}")

    async def create_group(
        self, phone_number: str, request: CreateGroupRequest
    ) -> dict[str, Any]:
        """Create a new Signal Group."""
        return await self._request(
            "POST", f"/v1/groups/{phone_number}", json=request.model_dump()
        )

    async def get_group(self, phone_number: str, group_id: str) -> dict[str, Any]:
        """List a Signal Group."""
        return await self._request("GET", f"/v1/groups/{phone_number}/{group_id}")

    async def update_group(
        self, phone_number: str, group_id: str, request: UpdateGroupRequest
    ) -> dict[str, Any]:
        """Update the state of a Signal Group."""
        return await self._request(
            "PUT",
            f"/v1/groups/{phone_number}/{group_id}",
            json=request.model_dump(),
        )

    async def delete_group(self, phone_number: str, group_id: str) -> dict[str, Any]:
        """Delete a Signal Group."""
        return await self._request("DELETE", f"/v1/groups/{phone_number}/{group_id}")

    async def add_admins(
        self, phone_number: str, group_id: str, request: ChangeGroupAdminsRequest
    ) -> dict[str, Any]:
        """Add admins to a group."""
        return await self._request(
            "POST",
            f"/v1/groups/{phone_number}/{group_id}/admins",
            json=request.model_dump(),
        )

    async def remove_admins(
        self, phone_number: str, group_id: str, request: ChangeGroupAdminsRequest
    ) -> dict[str, Any]:
        """Remove admins from a group."""
        return await self._request(
            "DELETE",
            f"/v1/groups/{phone_number}/{group_id}/admins",
            json=request.model_dump(),
        )

    async def get_avatar(self, phone_number: str, group_id: str) -> bytes:
        """Returns the avatar of a Signal Group."""
        return await self._request(
            "GET", f"/v1/groups/{phone_number}/{group_id}/avatar"
        )

    async def block(self, phone_number: str, group_id: str) -> dict[str, Any]:
        """Block a Signal Group."""
        return await self._request("POST", f"/v1/groups/{phone_number}/{group_id}/block")

    async def join(self, phone_number: str, group_id: str) -> dict[str, Any]:
        """Join a Signal Group."""
        return await self._request("POST", f"/v1/groups/{phone_number}/{group_id}/join")

    async def add_members(
        self, phone_number: str, group_id: str, request: ChangeGroupMembersRequest
    ) -> dict[str, Any]:
        """Add members to a group."""
        return await self._request(
            "POST",
            f"/v1/groups/{phone_number}/{group_id}/members",
            json=request.model_dump(),
        )

    async def remove_members(
        self, phone_number: str, group_id: str, request: ChangeGroupMembersRequest
    ) -> dict[str, Any]:
        """Remove members from a group."""
        return await self._request(
            "DELETE",
            f"/v1/groups/{phone_number}/{group_id}/members",
            json=request.model_dump(),
        )

    async def quit(self, phone_number: str, group_id: str) -> dict[str, Any]:
        """Quit a Signal Group."""
        return await self._request("POST", f"/v1/groups/{phone_number}/{group_id}/quit")