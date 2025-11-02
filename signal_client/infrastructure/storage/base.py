from abc import ABC, abstractmethod
from typing import Any


class Storage(ABC):
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def read(self, key: str) -> Any:
        pass

    @abstractmethod
    async def save(self, key: str, object: Any) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass


class StorageError(Exception):
    pass