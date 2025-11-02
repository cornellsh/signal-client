from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from signal_client.infrastructure.api_clients.reactions_client import ReactionsClient


@pytest.fixture
def reactions_client(mock_session: AsyncMock) -> ReactionsClient:
    return ReactionsClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_send_reaction(
    reactions_client: ReactionsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    reaction_data = {
        "recipient": "+0987654321",
        "action": "react",
        "emoji": "👍",
    }
    await reactions_client.send_reaction(phone_number, reaction_data)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/reactions/{phone_number}",
        json=reaction_data,
    )


@pytest.mark.asyncio
async def test_remove_reaction(
    reactions_client: ReactionsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    reaction_data = {
        "recipient": "+0987654321",
        "action": "react",
        "emoji": "👍",
    }
    await reactions_client.remove_reaction(phone_number, reaction_data)
    mock_session.request.assert_called_once_with(
        "DELETE",
        f"http://localhost:8080/v1/reactions/{phone_number}",
        json=reaction_data,
    )
