import pytest


@pytest.mark.anyio
async def test_create_user(user_repository):
    telegram_id = 12345
    name = "name"

    await user_repository.delete_user(telegram_id)

    try:
        await user_repository.create_user(telegram_id, name)

        user = await user_repository.get_user(telegram_id)

        assert user["telegram_id"] == telegram_id
        assert user["name"] == name
    finally:
        await user_repository.delete_user(telegram_id)


@pytest.mark.anyio
async def test_get_user_returns_none_if_user_does_not_exist(user_repository):
    telegram_id = 12345
    await user_repository.delete_user(telegram_id)

    try:
        user = await user_repository.get_user(telegram_id)
        assert user is None

    finally:
        await user_repository.delete_user(telegram_id)


@pytest.mark.anyio
async def test_delete_user(user_repository):
    telegram_id = 12345
    name = "name"

    await user_repository.delete_user(telegram_id)

    try:
        await user_repository.create_user(telegram_id, name)
        await user_repository.delete_user(telegram_id)

        user = await user_repository.get_user(telegram_id)

        assert user is None
    finally:
        await user_repository.delete_user(telegram_id)
