from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest


@pytest.fixture
def mock_session():
    """Fixture for a mocked aiohttp.ClientSession."""
    session = MagicMock(spec=aiohttp.ClientSession)
    mock_response = MagicMock()
    mock_response.content_type = "application/json"
    mock_response.json = AsyncMock(return_value={})
    mock_response.read = AsyncMock(return_value=b"")
    mock_response.raise_for_status = MagicMock()

    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_response
    session.request = MagicMock(return_value=mock_context_manager)
    return session
