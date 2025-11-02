from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    base64_attachments: list[str] = []
    message: str
    number: str
    recipients: list[str]
    link_preview: dict[str, Any] | None = None
    quote_author: str | None = None
    quote_mentions: list[str] | None = None
    quote_message: str | None = None
    quote_timestamp: int | None = None
    mentions: list[dict[str, Any]] | None = None
    text_mode: str | None = None
    edit_timestamp: int | None = None
    view_once: bool = False


class SendMessageResponse(BaseModel):
    timestamp: int


class GetGroupRequest(BaseModel):
    group_id: str


class UpdateGroupRequest(BaseModel):
    base64_avatar: str | None = None
    description: str | None = None
    expiration_in_seconds: int | None = None
    name: str | None = None


class CreateGroupRequest(BaseModel):
    name: str
    members: list[str]
    description: str | None = None
    permissions: dict[str, str] | None = None
    group_link: str | None = None
    expiration_time: int | None = None


class ChangeGroupAdminsRequest(BaseModel):
    admins: list[str]


class ChangeGroupMembersRequest(BaseModel):
    members: list[str]


class RemoteDeleteRequest(BaseModel):
    target_timestamp: int
    recipient: str | None = None
    group: str | None = None


class TypingIndicatorRequest(BaseModel):
    recipient: str | None = None
    group: str | None = None


class ReactionRequest(BaseModel):
    recipient: str | None = None
    group: str | None = None
    emoji: str
    target_author: str
    target_timestamp: int


class ReceiptRequest(BaseModel):
    recipient: str | None = None
    group: str | None = None
    target_timestamp: int
    type: str = "read"


class UpdateProfileRequest(BaseModel):
    name: str
    base64_avatar: str | None = None


class UpdateContactRequest(BaseModel):
    name: str
    number: str
    expiration_in_seconds: int | None = None
