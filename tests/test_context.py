from __future__ import annotations

from typing import cast
from unittest.mock import AsyncMock

import pytest

from signal_client import SignalClient
from signal_client.context import Context
from signal_client.entities import ContextDependencies
from signal_client.infrastructure.schemas.message import Message, MessageType
from signal_client.infrastructure.schemas.requests import SendMessageRequest


@pytest.mark.asyncio
async def test_context_send(bot: SignalClient):
    """Test that context.send calls the API service correctly."""
    # Arrange
    message = Message(
        message="test",
        source="user1",
        timestamp=1,
        type=MessageType.DATA_MESSAGE,
    )
    dependencies = ContextDependencies(
        accounts_client=bot.container.accounts_client(),
        attachments_client=bot.container.attachments_client(),
        contacts_client=bot.container.contacts_client(),
        devices_client=bot.container.devices_client(),
        general_client=bot.container.general_client(),
        groups_client=bot.container.groups_client(),
        identities_client=bot.container.identities_client(),
        messages_client=bot.container.messages_client(),
        profiles_client=bot.container.profiles_client(),
        reactions_client=bot.container.reactions_client(),
        receipts_client=bot.container.receipts_client(),
        search_client=bot.container.search_client(),
        sticker_packs_client=bot.container.sticker_packs_client(),
        lock_manager=bot.container.lock_manager(),
        phone_number=bot.container.config.phone_number(),
    )
    context = Context(
        message=message,
        dependencies=dependencies,
    )

    # Act
    request = SendMessageRequest(message="hello", recipients=[])
    await context.send(request)

    # Assert
    send_mock = cast("AsyncMock", bot.container.messages_client().send)
    (request_dict,) = send_mock.call_args.args
    assert request_dict["message"] == "hello"
    assert request_dict["recipients"] == ["user1"]


@pytest.mark.asyncio
async def test_context_reply(bot: SignalClient):
    """Test that context.reply calls the API service correctly."""
    # Arrange
    message = Message(
        message="test",
        source="user1",
        timestamp=1,
        type=MessageType.DATA_MESSAGE,
    )
    dependencies = ContextDependencies(
        accounts_client=bot.container.accounts_client(),
        attachments_client=bot.container.attachments_client(),
        contacts_client=bot.container.contacts_client(),
        devices_client=bot.container.devices_client(),
        general_client=bot.container.general_client(),
        groups_client=bot.container.groups_client(),
        identities_client=bot.container.identities_client(),
        messages_client=bot.container.messages_client(),
        profiles_client=bot.container.profiles_client(),
        reactions_client=bot.container.reactions_client(),
        receipts_client=bot.container.receipts_client(),
        search_client=bot.container.search_client(),
        sticker_packs_client=bot.container.sticker_packs_client(),
        lock_manager=bot.container.lock_manager(),
        phone_number=bot.container.config.phone_number(),
    )
    context = Context(
        message=message,
        dependencies=dependencies,
    )

    # Act
    request = SendMessageRequest(message="hello", recipients=[])
    await context.reply(request)

    # Assert
    send_mock = cast("AsyncMock", bot.container.messages_client().send)
    (request_dict,) = send_mock.call_args.args
    assert request_dict["message"] == "hello"
    assert request_dict["recipients"] == ["user1"]
    assert request_dict["quote_author"] == "user1"
    assert request_dict["quote_message"] == "test"
    assert request_dict["quote_timestamp"] == 1
