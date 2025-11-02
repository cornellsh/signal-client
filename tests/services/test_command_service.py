import asyncio
import re
from unittest.mock import AsyncMock

import pytest

from signal_client import SignalClient
from signal_client.command import Command
from signal_client.context import Context
from signal_client.domain.message import Message, MessageType


class MockCommand(Command):
    triggers: list[str | re.Pattern] = []
    whitelisted: list[str] = []
    case_sensitive: bool = False

    def __init__(self):
        self.handle = AsyncMock()

    async def handle(self, context: Context) -> None:
        await self.handle(context)


class TestCommandService:
    def test_register(self, bot: SignalClient):
        """Test that a command is correctly registered."""
        command = MockCommand()
        bot.container.command_service().register(command)
        assert command in bot.container.command_service()._commands

    @pytest.mark.asyncio
    async def test_process_messages_calls_handle(self, bot: SignalClient):
        """Test that process_messages calls the command's handle method."""
        # Arrange
        command = MockCommand()
        command.triggers = ["!test"]
        bot.container.command_service().register(command)

        message = Message(
            message="!test",
            source="user1",
            group="group1",
            timestamp=1672531200000,
            type=MessageType.DATA_MESSAGE,
        )
        await bot.container.command_service()._queue.put(message)

        # Act
        try:
            await asyncio.wait_for(
                bot.container.command_service().process_messages(), timeout=0.1
            )
        except asyncio.TimeoutError:
            pass

        # Assert
        command.handle.assert_called_once()
        context = command.handle.call_args[0][0]
        assert isinstance(context, Context)
        assert context.message == message

    @pytest.mark.parametrize(
        "text, trigger, case_sensitive, expected",
        [
            ("!ping", "!ping", False, True),
            ("!ping pong", "!ping", False, True),
            ("!PING", "!ping", False, True),
            ("!PING", "!ping", True, False),
            ("ping", "!ping", False, False),
            ("hello !ping", "!ping", False, False),
            ("say hello", re.compile(r"say \w+"), False, True),
            ("say", re.compile(r"say \w+"), False, False),
        ],
    )
    def test_should_trigger(
        self, bot: SignalClient, text, trigger, case_sensitive, expected
    ):
        """Test the _should_trigger method with various inputs."""
        # Arrange
        command = MockCommand()
        command.triggers = [trigger]
        command.case_sensitive = case_sensitive

        message = Message(
            message=text,
            source="user1",
            timestamp=1,
            type=MessageType.DATA_MESSAGE,
        )
        context = Context(
            message,
            bot.container.api_service(),
            bot.container.config.phone_number(),
        )

        # Act
        result = bot.container.command_service()._should_trigger(command, context)

        # Assert
        assert result is expected

    def test_should_trigger_whitelist(self, bot: SignalClient):
        """Test that the whitelist prevents triggering."""
        # Arrange
        command = MockCommand()
        command.triggers = ["!admin"]
        command.whitelisted = ["admin_user"]

        message_allowed = Message(
            message="!admin",
            source="admin_user",
            timestamp=1,
            type=MessageType.DATA_MESSAGE,
        )
        context_allowed = Context(
            message_allowed,
            bot.container.api_service(),
            bot.container.config.phone_number(),
        )

        message_denied = Message(
            message="!admin",
            source="random_user",
            timestamp=1,
            type=MessageType.DATA_MESSAGE,
        )
        context_denied = Context(
            message_denied,
            bot.container.api_service(),
            bot.container.config.phone_number(),
        )

        # Act
        result_allowed = bot.container.command_service()._should_trigger(
            command, context_allowed
        )
        result_denied = bot.container.command_service()._should_trigger(
            command, context_denied
        )

        # Assert
        assert result_allowed is True
        assert result_denied is False

    def test_should_not_trigger_on_non_text_message(self, bot: SignalClient):
        """Test that non-text messages do not trigger commands."""
        # Arrange
        command = MockCommand()
        command.triggers = ["!test"]

        message = Message(
            message=None, source="user1", timestamp=1, type=MessageType.DATA_MESSAGE
        )
        context = Context(
            message,
            bot.container.api_service(),
            bot.container.config.phone_number(),
        )

        # Act
        result = bot.container.command_service()._should_trigger(command, context)

        # Assert
        assert result is False