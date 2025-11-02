from __future__ import annotations

import asyncio

from ..domain.message import Message
from ..command import Command
from ..context import Context
from ..infrastructure.api_service import APIService


class CommandService:
    def __init__(
        self,
        queue: asyncio.Queue[Message],
        api_service: APIService,
        phone_number: str,
    ):
        self._queue = queue
        self._api_service = api_service
        self._phone_number = phone_number
        self._commands: list[Command] = []

    def register(self, command: Command):
        """Register a new command."""
        self._commands.append(command)

    async def process(self, message: Message):
        """Process a single message."""
        context = Context(message, self._api_service, self._phone_number)
        for command in self._commands:
            if self._should_trigger(command, context):
                await command.handle(context)

    async def process_messages(self):
        """Continuously process messages from the queue."""
        while True:
            message = await self._queue.get()
            try:
                await self.process(message)
            finally:
                self._queue.task_done()

    def _should_trigger(self, command: Command, context: Context) -> bool:
        """Determine if a command should be triggered by a message."""
        if not context.message.message or not isinstance(context.message.message, str):
            return False

        # Whitelist check
        if command.whitelisted and context.message.source not in command.whitelisted:
            return False

        # Trigger check
        text = context.message.message
        if not command.case_sensitive:
            text = text.lower()

        for trigger in command.triggers:
            if isinstance(trigger, str):
                if text.startswith(trigger):
                    return True
            elif hasattr(trigger, "search") and trigger.search(text):
                return True

        return False