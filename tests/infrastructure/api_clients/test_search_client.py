from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from signalbot.infrastructure.api_clients.search_client import SearchClient


@pytest.fixture
def search_client(mock_session):
    return SearchClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_search_registered_numbers(
    search_client: SearchClient, mock_session
):
    phone_number = "+1234567890"
    numbers_to_search = ["+0987654321"]
    await search_client.search_registered_numbers(phone_number, numbers_to_search)
    mock_session.request.assert_called_once_with(
        "GET",
        f"http://localhost:8080/v1/search/{phone_number}",
        params={"numbers": numbers_to_search},
    )