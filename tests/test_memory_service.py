import pytest

from services import MemoryService


@pytest.mark.anyio
async def test_history_limit(message_repository, user_repository):
    telegram_id = 111111

    await user_repository.delete_user(telegram_id)
    await user_repository.create_user(telegram_id, "TestUser")
    user = await user_repository.get_user(telegram_id)
    user_id = user["id"]

    memory_service = MemoryService(message_repository)

    try:
        for i in range(21):
            await memory_service.add_message(user_id, "user", f"Привет{i}")

        messages = await memory_service.get_messages(user_id)

        assert len(messages) == 20
        assert messages[0]["content"] == "Привет1"
        assert messages[-1]["content"] == "Привет20"
    finally:
        await memory_service.clear_history(user_id)
        await user_repository.delete_user(telegram_id)


@pytest.mark.anyio
async def test_users_have_separate_history(message_repository, user_repository):
    telegram_id_1 = 111111
    telegram_id_2 = 222222

    await user_repository.delete_user(telegram_id_1)
    await user_repository.delete_user(telegram_id_2)

    await user_repository.create_user(telegram_id_1, "TestUser")
    await user_repository.create_user(telegram_id_2, "TestUser")

    user1 = await user_repository.get_user(telegram_id_1)
    user2 = await user_repository.get_user(telegram_id_2)

    user1_id = user1["id"]
    user2_id = user2["id"]

    memory_service = MemoryService(message_repository)

    try:
        await memory_service.add_message(user1_id, "user", "Привет от первого")
        await memory_service.add_message(user2_id, "user", "Привет от второго")

        user_1_messages = await memory_service.get_messages(user1_id)
        user_2_messages = await memory_service.get_messages(user2_id)

        assert user_1_messages == [{"role": "user", "content": "Привет от первого"}]

        assert user_2_messages == [{"role": "user", "content": "Привет от второго"}]
    finally:
        await memory_service.clear_history(user1_id)
        await memory_service.clear_history(user2_id)
        await user_repository.delete_user(telegram_id_1)
        await user_repository.delete_user(telegram_id_2)


@pytest.mark.anyio
async def test_clear_history(message_repository, user_repository):
    telegram_id = 111111

    await user_repository.delete_user(telegram_id)
    await user_repository.create_user(telegram_id, "TestUser")

    user = await user_repository.get_user(telegram_id)
    user_id = user["id"]

    memory_service = MemoryService(message_repository)

    try:
        await memory_service.add_message(user_id, "user", "Привет")
        await memory_service.add_message(user_id, "assistant", "Здравствуйте!")

        await memory_service.clear_history(user_id)
        messages = await memory_service.get_messages(user_id)

        assert messages == []
    finally:
        await memory_service.clear_history(user_id)
        await user_repository.delete_user(telegram_id)
