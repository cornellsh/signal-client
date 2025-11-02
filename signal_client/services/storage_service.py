from __future__ import annotations

from typing import Any

from ..infrastructure.storage.base import Storage
from ..infrastructure.storage.sqlite import SQLiteStorage
from ..infrastructure.storage.redis import RedisStorage


class StorageService:
    def __init__(self, config: dict):
        storage_type = config.get("type", "in-memory")
        if storage_type == "sqlite":
            self._storage: Storage = SQLiteStorage(config["sqlite_db"])
        elif storage_type == "redis":
            self._storage = RedisStorage(config["redis_host"], config["redis_port"])
        else:
            self._storage = SQLiteStorage()  # In-memory SQLite

    async def exists(self, key: str) -> bool:
        return await self._storage.exists(key)

    async def read(self, key: str) -> Any:
        return await self._storage.read(key)

    async def save(self, key: str, object: Any) -> None:
        await self._storage.save(key, object)

    async def delete(self, key: str) -> None:
        await self._storage.delete(key)