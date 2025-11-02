from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from signal_client.domain.messages import SendMessageRequest
from signal_client.infrastructure.api_clients.messages_client import MessagesClient


@pytest.fixture
def messages_client(mock_session: AsyncMock) -> MessagesClient:
    return MessagesClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_send(messages_client: MessagesClient, mock_session: AsyncMock) -> None:
    request = SendMessageRequest(
        number="+1234567890",
        recipients=["+0987654321"],
        message="Hello",
    )
    await messages_client.send(request.model_dump())
    mock_session.request.assert_called_once_with(
        "POST",
        "http://localhost:8080/v2/send",
        json=request.model_dump(),
    )
