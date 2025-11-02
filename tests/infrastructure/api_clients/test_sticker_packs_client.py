from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from signal_client.infrastructure.api_clients.sticker_packs_client import (
    StickerPacksClient,
)


@pytest.fixture
def sticker_packs_client(mock_session: AsyncMock) -> StickerPacksClient:
    return StickerPacksClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_get_sticker_packs(
    sticker_packs_client: StickerPacksClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    await sticker_packs_client.get_sticker_packs(phone_number)
    mock_session.request.assert_called_once_with(
        "GET", f"http://localhost:8080/v1/sticker-packs/{phone_number}"
    )


@pytest.mark.asyncio
async def test_add_sticker_pack(
    sticker_packs_client: StickerPacksClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    pack_data = {"pack_id": "test_pack"}
    await sticker_packs_client.add_sticker_pack(phone_number, pack_data)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/sticker-packs/{phone_number}",
        json=pack_data,
    )
