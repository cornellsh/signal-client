import json
from typing import Any

import redis

from .base import Storage, StorageError


class RedisStorage(Storage):
    def __init__(self, host: str, port: int):
        self._redis = redis.Redis(host=host, port=port, db=0)

    async def exists(self, key: str) -> bool:
        return await self._redis.exists(key)

    async def read(self, key: str) -> Any:
        try:
            result_bytes = await self._redis.get(key)
            result_str = result_bytes.decode("utf-8")
            result_dict = json.loads(result_str)
            return result_dict
        except Exception as e:
            raise StorageError(f"Redis load failed: {e}")

    async def save(self, key: str, object: Any) -> None:
        try:
            object_str = json.dumps(object)
            await self._redis.set(key, object_str)
        except Exception as e:
            raise StorageError(f"Redis save failed: {e}")

    async def delete(self, key: str) -> None:
        try:
            await self._redis.delete(key)
        except Exception as e:
            raise StorageError(f"Redis delete failed: {e}")