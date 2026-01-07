import uuid
import re
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MessageType(Enum):
    DATA_MESSAGE = "DATA_MESSAGE"
    SYNC_MESSAGE = "SYNC_MESSAGE"
    EDIT_MESSAGE = "EDIT_MESSAGE"
    DELETE_MESSAGE = "DELETE_MESSAGE"


class AttachmentPointer(BaseModel):
    id: str
    content_type: Optional[str] = Field(default=None, alias="contentType")
    filename: Optional[str] = None
    size: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    @field_validator("size", mode="before")
    @classmethod
    def normalize_size(cls, value: object) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return None
        return None


class Quote(BaseModel):
    id: int
    author: str
    text: Optional[str] = None
    attachments: Optional[List[AttachmentPointer]] = None

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class Message(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    message: Optional[str] = None
    source: str
    destination: Optional[str] = None
    timestamp: int
    type: MessageType
    group: Optional[dict] = Field(default=None, alias="groupInfo")
    reaction_emoji: Optional[str] = None
    target_sent_timestamp: Optional[int] = None
    remote_delete_timestamp: Optional[int] = None
    reaction_target_author: Optional[str] = None
    reaction_target_timestamp: Optional[int] = None
    attachments_local_filenames: Optional[List[str]] = None
    attachments: Optional[List[AttachmentPointer]] = None
    mentions: Optional[List[str]] = None
    quote: Optional[Quote] = None

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    @field_validator("attachments_local_filenames", mode="before")
    @classmethod
    def clean_attachments(cls, v: object) -> object:
        if isinstance(v, list):
            return [i for i in v if isinstance(i, str)]
        return v

    @staticmethod
    def normalize_number(n: Optional[str]) -> Optional[str]:
        if not n or not isinstance(n, str): return n
        if n.startswith("+") or "-" in n or n.endswith("="): 
            return n
        if n.isdigit():
            return f"+{n}"
        return n

    def recipient(self) -> str:
        if self.is_group() and self.group:
            return self.group["groupId"]
        return self.destination if self.destination and self.destination != self.source else self.source

    def is_group(self) -> bool:
        return self.group is not None

    def is_private(self) -> bool:
        return not self.is_group()

    @property
    def is_sync(self) -> bool:
        return self.type == MessageType.SYNC_MESSAGE

    def is_self(self, own_number: str) -> bool:
        own_norm = self.normalize_number(own_number)
        src_norm = self.normalize_number(self.source)
        return src_norm == own_norm or self.is_sync

    def is_reply_to(self, number: str) -> bool:
        if not self.quote:
            return False
        return self.normalize_number(self.quote.author) == self.normalize_number(number)

    def get_target_chat(self, own_number: str) -> str:
        own_norm = self.normalize_number(own_number)
        if self.is_group():
            return self.recipient()
        if self.is_self(own_number):
            dest_norm = self.normalize_number(self.destination)
            return dest_norm if dest_norm and dest_norm != own_norm else own_norm
        return self.normalize_number(self.source)

    def get_history_key(self, own_number: str) -> str:
        """Alias for get_target_chat to provide a stable key for conversation storage."""
        return self.get_target_chat(own_number)
