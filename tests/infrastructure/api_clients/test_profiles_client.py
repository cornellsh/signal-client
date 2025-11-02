from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from signal_client.infrastructure.api_clients.profiles_client import ProfilesClient


@pytest.fixture
def profiles_client(mock_session: AsyncMock) -> ProfilesClient:
    return ProfilesClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_update_profile(
    profiles_client: ProfilesClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    profile_data = {"name": "test"}
    await profiles_client.update_profile(phone_number, profile_data)
    mock_session.request.assert_called_once_with(
        "PUT",
        f"http://localhost:8080/v1/profiles/{phone_number}",
        json=profile_data,
    )
