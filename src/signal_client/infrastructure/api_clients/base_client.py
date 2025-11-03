from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import aiohttp
import structlog

from signal_client.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ServerError,
)

if TYPE_CHECKING:
    from signal_client.services.rate_limiter import RateLimiter


HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_SERVER_ERROR = 500


log = structlog.get_logger()


@dataclass
class ClientConfig:
    session: aiohttp.ClientSession
    base_url: str
    retries: int = 3
    backoff_factor: float = 0.5
    timeout: int = 30
    rate_limiter: RateLimiter | None = None


class BaseClient:
    def __init__(
        self,
        client_config: ClientConfig,
    ) -> None:
        self._session = client_config.session
        self._base_url = client_config.base_url
        self._retries = client_config.retries
        self._backoff_factor = client_config.backoff_factor
        self._timeout = aiohttp.ClientTimeout(total=client_config.timeout)
        self._rate_limiter = client_config.rate_limiter

    async def _handle_response(
        self, response: aiohttp.ClientResponse
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        if response.status >= HTTP_STATUS_BAD_REQUEST:
            body = await response.text()
            msg = (
                f"API request failed with status {response.status} "
                f"for URL {response.url}: {body}"
            )
            if response.status == HTTP_STATUS_UNAUTHORIZED:
                raise AuthenticationError(msg)
            if response.status == HTTP_STATUS_NOT_FOUND:
                raise NotFoundError(msg)
            if response.status >= HTTP_STATUS_SERVER_ERROR:
                raise ServerError(msg)
            raise APIError(msg)

        if response.content_type == "application/json":
            return await response.json()
        return await response.read()

    async def _make_request(
        self,
        method: str,
        path: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        url = f"{self._base_url}{path}"
        last_exc: Exception | None = None

        if self._rate_limiter:
            await self._rate_limiter.acquire()

        for attempt in range(self._retries + 1):
            async with self._session.request(
                method, url, timeout=self._timeout, **kwargs
            ) as response:
                try:
                    return await self._handle_response(response)
                except (aiohttp.ClientError, ServerError, asyncio.TimeoutError) as e:
                    last_exc = e
                    if attempt < self._retries:
                        delay = self._backoff_factor * (2**attempt)
                        log.warning(
                            "Request failed, retrying...",
                            attempt=attempt + 1,
                            max_retries=self._retries,
                            delay=delay,
                            exc_info=e,
                        )
                        await asyncio.sleep(delay)
                    else:
                        log.exception(
                            "Request failed after max retries",
                            attempt=attempt,
                        )

        msg = f"Request failed after {self._retries} retries"
        raise APIError(msg) from last_exc
