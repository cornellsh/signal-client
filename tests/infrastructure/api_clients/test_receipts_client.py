from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from signalbot.infrastructure.api_clients.receipts_client import ReceiptsClient


@pytest.fixture
def receipts_client(mock_session):
    return ReceiptsClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_send_receipt(receipts_client: ReceiptsClient, mock_session):
    phone_number = "+1234567890"
    receipt_data = {"recipient": "+0987654321"}
    await receipts_client.send_receipt(phone_number, receipt_data)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/receipts/{phone_number}",
        json=receipt_data,
    )