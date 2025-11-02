from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from signal_client.domain.groups import (
    ChangeGroupAdminsRequest,
    ChangeGroupMembersRequest,
    CreateGroupRequest,
    UpdateGroupRequest,
)
from signal_client.infrastructure.api_clients.groups_client import GroupsClient


@pytest.fixture
def groups_client(mock_session: AsyncMock) -> GroupsClient:
    return GroupsClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_create_group(
    groups_client: GroupsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    request = CreateGroupRequest(name="Test Group", members=[phone_number])
    await groups_client.create_group(phone_number, request)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/groups/{phone_number}",
        json=request.model_dump(),
    )


@pytest.mark.asyncio
async def test_update_group(
    groups_client: GroupsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    group_id = "group_id"
    request = UpdateGroupRequest(name="New Name")
    await groups_client.update_group(phone_number, group_id, request)
    mock_session.request.assert_called_once_with(
        "PUT",
        f"http://localhost:8080/v1/groups/{phone_number}/{group_id}",
        json=request.model_dump(),
    )


@pytest.mark.asyncio
async def test_add_members(
    groups_client: GroupsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    group_id = "group_id"
    request = ChangeGroupMembersRequest(members=[phone_number])
    await groups_client.add_members(phone_number, group_id, request)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/groups/{phone_number}/{group_id}/members",
        json=request.model_dump(),
    )


@pytest.mark.asyncio
async def test_remove_members(
    groups_client: GroupsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    group_id = "group_id"
    request = ChangeGroupMembersRequest(members=[phone_number])
    await groups_client.remove_members(phone_number, group_id, request)
    mock_session.request.assert_called_once_with(
        "DELETE",
        f"http://localhost:8080/v1/groups/{phone_number}/{group_id}/members",
        json=request.model_dump(),
    )


@pytest.mark.asyncio
async def test_add_admins(groups_client: GroupsClient, mock_session: AsyncMock) -> None:
    phone_number = "+1234567890"
    group_id = "group_id"
    request = ChangeGroupAdminsRequest(admins=[phone_number])
    await groups_client.add_admins(phone_number, group_id, request)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/groups/{phone_number}/{group_id}/admins",
        json=request.model_dump(),
    )
