from __future__ import annotations

from pathlib import Path

import pytest

from signal_client.infrastructure.schemas.message import AttachmentPointer
from signal_client.services.attachment_downloader import (
    AttachmentDownloadError,
    AttachmentDownloader,
)


class _FakeAttachmentsClient:
    def __init__(self, blobs: dict[str, bytes]) -> None:
        self._blobs = blobs

    async def get_attachment(self, attachment_id: str) -> bytes:
        return self._blobs[attachment_id]


@pytest.mark.asyncio
async def test_download_and_cleanup_tempdir(tmp_path: Path) -> None:
    attachments = [
        AttachmentPointer(id="one", filename="one.txt"),
        AttachmentPointer(id="two"),
    ]
    client = _FakeAttachmentsClient({"one": b"1", "two": b"22"})
    downloader = AttachmentDownloader(client, max_total_bytes=10)

    async with downloader.download(attachments) as files:
        assert [file.name for file in files] == ["one.txt", "two"]
        for file in files:
            assert file.exists()
            assert file.read_bytes()

    for file in files:
        assert not file.exists()
        assert not file.parent.exists()


@pytest.mark.asyncio
async def test_download_with_destination_dir(tmp_path: Path) -> None:
    attachments = [AttachmentPointer(id="one", filename="keep.bin")]
    client = _FakeAttachmentsClient({"one": b"123"})
    downloader = AttachmentDownloader(client)

    dest = tmp_path / "attachments"
    async with downloader.download(attachments, dest_dir=dest) as files:
        assert files[0].parent == dest
        assert files[0].read_bytes() == b"123"

    # Caller-managed destination should remain intact.
    assert dest.exists()
    assert (dest / "keep.bin").exists()


@pytest.mark.asyncio
async def test_download_exceeds_limit(tmp_path: Path) -> None:
    attachments = [AttachmentPointer(id="one", filename="large.bin")]
    client = _FakeAttachmentsClient({"one": b"x" * 5})
    downloader = AttachmentDownloader(client, max_total_bytes=1)

    with pytest.raises(AttachmentDownloadError):
        async with downloader.download(attachments) as _:
            pass
