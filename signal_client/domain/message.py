from __future__ import annotations

import json
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from ..link_previews import LinkPreview
from .quote import Quote


class MessageType(Enum):
    SYNC_MESSAGE = 1  # Message recieved in a linked device
    DATA_MESSAGE = 2  # Message recieved in a primary device
    EDIT_MESSAGE = 3  # Message received is an edit of a previous message
    DELETE_MESSAGE = 4  # Message received is a remote delete of a previous message


class Message(BaseModel):
    # Core fields from envelope
    source: str
    timestamp: int
    type: MessageType
    source_number: Optional[str] = None
    source_uuid: Optional[str] = None

    # Core fields from dataMessage
    message: Optional[str] = None
    group: Optional[str] = None
    view_once: bool = False
    mentions: list[str] = Field(default_factory=list)
    attachments_local_filenames: list[str] = Field(default_factory=list)
    base64_attachments: list[str] = Field(default_factory=list)
    link_previews: list[LinkPreview] = Field(default_factory=list)

    # Special message type fields
    quote: Optional[Quote] = None
    reaction_emoji: Optional[str] = None
    reaction_target_author: Optional[str] = None
    reaction_target_timestamp: Optional[int] = None
    target_sent_timestamp: Optional[int] = None  # For edits
    remote_delete_timestamp: Optional[int] = None  # For deletes

    # Metadata
    raw_message: Optional[str] = None

    def recipient(self) -> str:
        # Case 1: Group chat
        if self.group:
            return self.group  # internal ID

        # Case 2: User chat
        return self.source

    def is_private(self) -> bool:
        return not bool(self.group)

    def is_group(self) -> bool:
        return bool(self.group)

    def __str__(self) -> str:
        if self.message is None:
            return ""
        return self.message
