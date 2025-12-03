from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING


@dataclass(slots=True)
class QueuedMessage:
    raw: str
    enqueued_at: float
    recipient: str | None = None
    message: "Message | None" = None
    ack: Callable[[], None] | None = None


__all__ = ["QueuedMessage"]

if TYPE_CHECKING:  # pragma: no cover - circular import guard
    from signal_client.infrastructure.schemas.message import Message
