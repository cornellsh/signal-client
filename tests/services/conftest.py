from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest

from signal_client import SignalClient
from signal_client.domain.message import Message


@pytest.fixture
def bot() -> SignalClient:
    """Return a SignalClient instance."""
    return SignalClient(
        config={
            "signal_service": "localhost:8080",
            "phone_number": "+1234567890",
            "storage": {"type": "in-memory"},
        }
    )


@pytest.fixture
def mock_session() -> AsyncMock:
    """Return a mock aiohttp session."""
    return AsyncMock()


@pytest.fixture
def message_queue() -> asyncio.Queue[Message]:
    """Return a message queue."""
    return asyncio.Queue()
