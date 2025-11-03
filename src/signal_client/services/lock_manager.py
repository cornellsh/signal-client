from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager


class LockManager:
    """A manager for asyncio.Lock objects to prevent race conditions."""

    def __init__(self) -> None:
        self._locks: dict[str, asyncio.Lock] = {}
        self._manager_lock = asyncio.Lock()

    @asynccontextmanager
    async def lock(self, resource_id: str) -> AsyncGenerator[None, None]:
        """Acquire a lock for a specific resource."""
        async with self._manager_lock:
            if resource_id not in self._locks:
                self._locks[resource_id] = asyncio.Lock()

        resource_lock = self._locks[resource_id]
        async with resource_lock:
            yield
