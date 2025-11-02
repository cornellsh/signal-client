from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from signal_client.infrastructure.api_clients.accounts_client import AccountsClient


@pytest.fixture
def accounts_client(mock_session: AsyncMock) -> AccountsClient:
    return AccountsClient(mock_session, "http://localhost:8080")


@pytest.mark.asyncio
async def test_get_accounts(
    accounts_client: AccountsClient, mock_session: AsyncMock
) -> None:
    mock_session.request.return_value.__aenter__.return_value.json.return_value = []
    result = await accounts_client.get_accounts()
    mock_session.request.assert_called_once_with(
        "GET", "http://localhost:8080/v1/accounts"
    )
    assert result == []


@pytest.mark.asyncio
async def test_set_pin(
    accounts_client: AccountsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    pin_data = {"pin": "1234"}
    await accounts_client.set_pin(phone_number, pin_data)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/accounts/{phone_number}/pin",
        json=pin_data,
    )


@pytest.mark.asyncio
async def test_remove_pin(
    accounts_client: AccountsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    await accounts_client.remove_pin(phone_number)
    mock_session.request.assert_called_once_with(
        "DELETE", f"http://localhost:8080/v1/accounts/{phone_number}/pin"
    )


@pytest.mark.asyncio
async def test_lift_rate_limit(
    accounts_client: AccountsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    captcha_data = {"captcha": "test"}
    await accounts_client.lift_rate_limit(phone_number, captcha_data)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/accounts/{phone_number}/rate-limit-challenge",
        json=captcha_data,
    )


@pytest.mark.asyncio
async def test_update_settings(
    accounts_client: AccountsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    settings_data = {"theme": "dark"}
    await accounts_client.update_settings(phone_number, settings_data)
    mock_session.request.assert_called_once_with(
        "PUT",
        f"http://localhost:8080/v1/accounts/{phone_number}/settings",
        json=settings_data,
    )


@pytest.mark.asyncio
async def test_set_username(
    accounts_client: AccountsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    username_data = {"username": "test"}
    await accounts_client.set_username(phone_number, username_data)
    mock_session.request.assert_called_once_with(
        "POST",
        f"http://localhost:8080/v1/accounts/{phone_number}/username",
        json=username_data,
    )


@pytest.mark.asyncio
async def test_remove_username(
    accounts_client: AccountsClient, mock_session: AsyncMock
) -> None:
    phone_number = "+1234567890"
    await accounts_client.remove_username(phone_number)
    mock_session.request.assert_called_once_with(
        "DELETE", f"http://localhost:8080/v1/accounts/{phone_number}/username"
    )
