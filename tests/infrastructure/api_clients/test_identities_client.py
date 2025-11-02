from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from signalbot.infrastructure.api_clients.identities_client import IdentitiesClient


@pytest.fixture
def identities_client(mock_session):
    return IdentitiesClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_get_identities(identities_client: IdentitiesClient, mock_session):
    phone_number = "+1234567890"
    await identities_client.get_identities(phone_number)
    mock_session.request.assert_called_once_with(
        "GET", f"http://localhost:8080/v1/identities/{phone_number}"
    )


@pytest.mark.asyncio
async def test_trust_identity(identities_client: IdentitiesClient, mock_session):
    phone_number = "+1234567890"
    number_to_trust = "+0987654321"
    trust_data = {"verified": True}
    await identities_client.trust_identity(phone_number, number_to_trust, trust_data)
    mock_session.request.assert_called_once_with(
        "PUT",
        f"http://localhost:8080/v1/identities/{phone_number}/trust/{number_to_trust}",
        json=trust_data,
    )