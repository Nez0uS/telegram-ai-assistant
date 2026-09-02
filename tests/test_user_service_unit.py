from unittest.mock import AsyncMock, Mock
import pytest

from services import UserService


@pytest.mark.anyio
async def test_register_user_creates_new_user():
    telegram_id = 123456
    name = "name"

    repository = Mock()

    repository.get_user = AsyncMock(return_value=None)
    repository.create_user = AsyncMock()

    user_service = UserService(repository)

    await user_service.register_user(telegram_id, name)

    repository.get_user.assert_awaited_once_with(telegram_id)
    repository.create_user.assert_awaited_once_with(
        telegram_id,
        name
    )


@pytest.mark.anyio
async def test_register_user_does_not_create_existing_user():
    telegram_id = 123456
    name = "name"

    repository = Mock()
    repository.get_user = AsyncMock(
        return_value={
            "telegram_id": telegram_id,
            "name": name
        }
    )

    repository.create_user = AsyncMock()
    user_service = UserService(repository)

    await user_service.register_user(telegram_id, name)

    repository.create_user.assert_not_awaited()
    repository.get_user.assert_awaited_once_with(telegram_id)


@pytest.mark.anyio
async def test_get_user_returns_user():
    telegram_id = 123456
    name = "name"

    expected_user = {
        "telegram_id": telegram_id,
        "name": name
    }

    repository = Mock()
    repository.get_user = AsyncMock(
        return_value=expected_user
    )

    user_service = UserService(repository)

    result = await user_service.get_user(telegram_id)
    assert result == expected_user
    repository.get_user.assert_awaited_once_with(telegram_id)
