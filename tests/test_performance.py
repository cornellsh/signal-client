import asyncio
import json
import time
import uuid
from typing import ClassVar

import pytest
from tqdm import tqdm

from signal_client.command import Command
from signal_client.container import Container
from signal_client.context import Context

# Configuration for the load test
NUM_MESSAGES = 100  # A much smaller number for debugging
WORKER_POOL_SIZE = 4  # Number of workers to use for the test
QUEUE_SIZE = 100  # Match the number of messages for this test
MIN_MESSAGES_PER_SECOND = 50


class MockCommand(Command):
    """A mock command that simulates some async work."""

    triggers: ClassVar[list[str]] = ["!mock"]
    whitelisted: ClassVar[list[str]] = []
    case_sensitive = False

    async def handle(self, _: Context) -> None:
        # Simulate a small amount of I/O-bound work (e.g., an API call)
        await asyncio.sleep(0.01)
        # Use the lock manager to simulate a real-world command
        # async with context.lock(context.message.source):
        #     # Simulate some work inside the lock
        await asyncio.sleep(0.01)


@pytest.mark.timeout(0)
@pytest.mark.asyncio
async def test_performance(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    A load test to measure the performance of the message processing pipeline.
    """
    # Mock the websocket client to prevent it from trying to connect
    monkeypatch.setattr(
        "signal_client.container.WebSocketClient.__init__", lambda *_, **__: None
    )

    # Set up the container with the test configuration
    container = Container()
    container.config.from_dict(
        {
            "worker_pool_size": WORKER_POOL_SIZE,
            "queue_size": QUEUE_SIZE,
            "phone_number": "+1234567890",
            "base_url": "http://mock-server",
            "signal_service": "ws://mock-server",
        }
    )

    # Register the mock command
    worker_pool_manager = container.worker_pool_manager()
    worker_pool_manager.register(MockCommand())

    # Start the worker pool
    worker_pool_manager.start()

    # Get the message queue
    queue = container.message_queue()

    # Generate a large number of mock messages
    # Generate a large number of mock messages
    messages = [
        {
            "envelope": {
                "source": f"+1000000{i % 100}",  # Simulate 100 different users
                "sourceDevice": 1,
                "timestamp": int(time.time() * 1000),
                "dataMessage": {
                    "message": "!mock",
                    "timestamp": int(time.time() * 1000),
                },
            },
            "syncMessage": {},
            "type": "SYNC_MESSAGE",
            "id": str(uuid.uuid4()),
        }
        for i in range(NUM_MESSAGES)
    ]

    # Start the timer
    start_time = time.monotonic()

    # Put messages on the queue with a progress bar
    for message in tqdm(messages, desc="Queueing messages"):
        await queue.put(json.dumps(message))

    # Wait for all messages to be processed
    # Wait for all messages to be processed
    await queue.join()

    # Stop the timer
    end_time = time.monotonic()

    # Stop the worker pool
    worker_pool_manager.stop()
    await worker_pool_manager.join()

    # Clean up the session
    session = container.session()
    await session.close()

    # Calculate and print the performance metrics
    duration = end_time - start_time
    messages_per_second = NUM_MESSAGES / duration

    print("\n--- Load Test Results ---")
    print(f"Processed {NUM_MESSAGES} messages in {duration:.2f} seconds.")
    print(f"Messages per second: {messages_per_second:.2f}")
    print(f"Worker pool size: {WORKER_POOL_SIZE}")
    print("-----------------------")

    # Assert that the performance is within a reasonable range
    # This is a baseline; it can be adjusted as the library is optimized.
    assert messages_per_second > MIN_MESSAGES_PER_SECOND
