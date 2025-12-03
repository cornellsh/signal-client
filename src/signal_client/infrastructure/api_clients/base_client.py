from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Mapping

from yarl import URL

import aiohttp
import structlog

from signal_client.exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from signal_client.observability.metrics import API_CLIENT_PERFORMANCE

if TYPE_CHECKING:
    from signal_client.services.circuit_breaker import CircuitBreaker
    from signal_client.services.rate_limiter import RateLimiter


HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_CONFLICT = 409
HTTP_STATUS_TOO_MANY_REQUESTS = 429
HTTP_STATUS_SERVER_ERROR = 500

ERROR_CODE_MAP: dict[str, tuple[type[APIError], str | None]] = {
    "USER_NOT_GROUP_MEMBER": (
        ConflictError,
        "docs.signal-client.dev/errors#user-not-a-group-member",
    ),
    "USERNAME_ALREADY_TAKEN": (
        ConflictError,
        "docs.signal-client.dev/errors#username-already-taken",
    ),
    "GROUP_NOT_FOUND": (
        NotFoundError,
        "docs.signal-client.dev/errors#group-not-found",
    ),
    "ATTACHMENT_NOT_FOUND": (
        NotFoundError,
        "docs.signal-client.dev/errors#attachment-not-found",
    ),
    "CONTACT_NOT_FOUND": (
        NotFoundError,
        "docs.signal-client.dev/errors#contact-not-found",
    ),
    "RATE_LIMIT_EXCEEDED": (
        RateLimitError,
        "docs.signal-client.dev/errors#rate-limit-exceeded",
    ),
    "INTERNAL_SERVER_ERROR": (
        ServerError,
        "docs.signal-client.dev/errors#server-error",
    ),
}

ERROR_STATUS_MAP: dict[int, tuple[type[APIError], str]] = {
    HTTP_STATUS_UNAUTHORIZED: (
        AuthenticationError,
        "docs.signal-client.dev/errors#authentication-error",
    ),
    HTTP_STATUS_NOT_FOUND: (
        NotFoundError,
        "docs.signal-client.dev/errors#not-found-error",
    ),
    HTTP_STATUS_CONFLICT: (
        ConflictError,
        "docs.signal-client.dev/errors#conflict-error",
    ),
    HTTP_STATUS_TOO_MANY_REQUESTS: (
        RateLimitError,
        "docs.signal-client.dev/errors#rate-limit-error",
    ),
}


log = structlog.get_logger()


HeaderProvider = Callable[[str, str], Awaitable[Mapping[str, str]] | Mapping[str, str]]


@dataclass(slots=True)
class RequestOptions:
    timeout: float | None = None
    retries: int | None = None
    backoff_factor: float | None = None
    idempotency_key: str | None = None
    headers: Mapping[str, str] | None = None


@dataclass
class ClientConfig:
    session: aiohttp.ClientSession
    base_url: str
    retries: int = 3
    backoff_factor: float = 0.5
    timeout: int = 30
    rate_limiter: RateLimiter | None = None
    circuit_breaker: CircuitBreaker | None = None
    default_headers: Mapping[str, str] | None = None
    header_provider: HeaderProvider | None = None
    endpoint_timeouts: Mapping[str, float] | None = None
    idempotency_header_name: str = "Idempotency-Key"


class BaseClient:
    def __init__(
        self,
        client_config: ClientConfig,
    ) -> None:
        self._session = client_config.session
        self._base_url = client_config.base_url.rstrip("/")
        self._retries = client_config.retries
        self._backoff_factor = client_config.backoff_factor
        self._default_timeout_seconds = float(client_config.timeout)
        self._rate_limiter = client_config.rate_limiter
        self._circuit_breaker = client_config.circuit_breaker
        self._default_headers: dict[str, str] = (
            dict(client_config.default_headers) if client_config.default_headers else {}
        )
        self._header_provider = client_config.header_provider
        self._endpoint_timeouts: dict[str, float] = (
            {
                path: float(timeout)
                for path, timeout in (client_config.endpoint_timeouts or {}).items()
                if timeout is not None
            }
        )
        self._idempotency_header_name = client_config.idempotency_header_name

    async def _handle_response(
        self, response: aiohttp.ClientResponse
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        if response.status >= HTTP_STATUS_BAD_REQUEST:
            payload, error_message = await self._extract_error_payload(response)
            normalized_code = self._normalize_error_code(payload)
            response_body = self._serialize_error_body(payload, error_message)
            error_text = error_message or normalized_code or f"HTTP {response.status}"
            self._raise_for_error(
                response.status, error_text, response_body, normalized_code
            )

        if response.content_type == "application/json":
            return await response.json()
        return await response.read()

    async def _extract_error_payload(
        self, response: aiohttp.ClientResponse
    ) -> tuple[object | None, str]:
        try:
            payload = await response.json()
        except aiohttp.ContentTypeError:
            text_payload = await response.text()
            return None, text_payload

        if isinstance(payload, dict):
            message = str(payload.get("error") or payload.get("message") or "")
            return payload, message
        if isinstance(payload, list):
            serialized = json.dumps(payload)
            return payload, serialized
        return payload, str(payload)

    @staticmethod
    def _normalize_error_code(payload: object | None) -> str | None:
        if isinstance(payload, dict):
            raw_code = payload.get("code")
            if isinstance(raw_code, str):
                return raw_code.strip().replace("-", "_").replace(" ", "_").upper()
        return None

    @staticmethod
    def _serialize_error_body(payload: object | None, fallback: str) -> str:
        if isinstance(payload, (dict, list)):
            return json.dumps(payload)
        return fallback

    def _raise_for_error(
        self,
        status: int,
        error_text: str,
        response_body: str,
        normalized_code: str | None,
    ) -> None:
        if normalized_code and normalized_code in ERROR_CODE_MAP:
            exc_cls, docs_url = ERROR_CODE_MAP[normalized_code]
            raise exc_cls(
                message=error_text,
                status_code=status,
                response_body=response_body,
                docs_url=docs_url,
            )

        if status in ERROR_STATUS_MAP:
            exc_cls, docs_url = ERROR_STATUS_MAP[status]
            raise exc_cls(
                message=error_text,
                status_code=status,
                response_body=response_body,
                docs_url=docs_url,
            )

        if status >= HTTP_STATUS_SERVER_ERROR:
            raise ServerError(
                message=error_text,
                status_code=status,
                response_body=response_body,
                docs_url="docs.signal-client.dev/errors#server-error",
            )

        raise APIError(
            message=error_text,
            status_code=status,
            response_body=response_body,
            docs_url="docs.signal-client.dev/errors#api-error",
        )

    async def _make_request(
        self,
        method: str,
        path: str,
        *,
        request_options: RequestOptions | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        url = str(URL(self._base_url) / path.lstrip("/"))
        effective_timeout = self._resolve_timeout(path, request_options)
        retries = request_options.retries if request_options else None
        backoff_factor = request_options.backoff_factor if request_options else None
        headers = await self._headers_for_request(
            method=method,
            path=path,
            request_options=request_options,
            explicit_headers=kwargs.pop("headers", None),
        )
        if headers:
            kwargs["headers"] = headers

        if self._rate_limiter:
            await self._rate_limiter.acquire()

        with API_CLIENT_PERFORMANCE.time():
            if self._circuit_breaker:
                async with self._circuit_breaker.guard(path):
                    return await self._send_request_with_retries(
                        method,
                        url,
                        timeout_seconds=effective_timeout,
                        retries=retries,
                        backoff_factor=backoff_factor,
                        **kwargs,
                    )
            return await self._send_request_with_retries(
                method,
                url,
                timeout_seconds=effective_timeout,
                retries=retries,
                backoff_factor=backoff_factor,
                **kwargs,
            )

    async def _send_single_request(
        self,
        method: str,
        url: str,
        timeout_seconds: float,
        **kwargs: Any,  # noqa: ANN401
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes | Exception:
        timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        try:
            async with self._session.request(
                method, url, timeout=timeout, **kwargs
            ) as response:
                return await self._handle_response(response)
        except (aiohttp.ClientError, ServerError, asyncio.TimeoutError) as e:
            return e

    async def _send_request_with_retries(
        self,
        method: str,
        url: str,
        *,
        timeout_seconds: float,
        retries: int | None = None,
        backoff_factor: float | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        resolved_retries = self._retries if retries is None else retries
        resolved_backoff = (
            self._backoff_factor if backoff_factor is None else backoff_factor
        )
        last_exc: Exception | None = None
        for attempt in range(resolved_retries + 1):
            result = await self._send_single_request(
                method, url, timeout_seconds=timeout_seconds, **kwargs
            )
            if not isinstance(result, Exception):
                return result

            last_exc = result
            if attempt < resolved_retries:
                delay = resolved_backoff * (2**attempt)
                log.warning(
                    "api_client.retrying",
                    method=method,
                    url=url,
                    attempt=attempt + 1,
                    max_retries=resolved_retries,
                    delay=delay,
                    exc_info=last_exc,
                )
                await asyncio.sleep(delay)
            else:
                log.exception(
                    "api_client.failed",
                    method=method,
                    url=url,
                    retries=resolved_retries,
                )
        if last_exc:
            raise last_exc
        msg = f"Request failed after {resolved_retries} retries"
        raise APIError(msg)

    async def _headers_for_request(
        self,
        *,
        method: str,
        path: str,
        request_options: RequestOptions | None,
        explicit_headers: Mapping[str, str] | None,
    ) -> dict[str, str]:
        headers: dict[str, str] = dict(self._default_headers)

        if self._header_provider:
            provided = self._header_provider(method, path)
            if asyncio.iscoroutine(provided):
                provided = await provided
            if provided:
                headers.update(dict(provided))

        if explicit_headers:
            headers.update(dict(explicit_headers))

        if request_options and request_options.headers:
            headers.update(dict(request_options.headers))

        idempotency_key = (
            request_options.idempotency_key if request_options else None
        )
        if idempotency_key:
            headers[self._idempotency_header_name] = idempotency_key

        return headers

    def _resolve_timeout(
        self, path: str, request_options: RequestOptions | None
    ) -> float:
        if request_options and request_options.timeout is not None:
            return float(request_options.timeout)

        for prefix, timeout in self._endpoint_timeouts.items():
            normalized_prefix = prefix.rstrip("/")
            if path.rstrip("/").startswith(normalized_prefix):
                return timeout

        return self._default_timeout_seconds
