import pytest

from database import Database
from services import MemoryService


@pytest.mark.anyio
async def test_history_limit():
    database = Database()
    await database.connect()

    user_id = 123

    try:
        await database.clear_history(user_id)

        memory_service = MemoryService(database)

        for i in range(21):
            await memory_service.add_message(
                user_id,
                "user",
                f"Привет{i}"
            )

        messages = await memory_service.get_messages(user_id)

        assert len(messages) == 20
        assert messages[0]["content"] == "Привет1"
        assert messages[-1]["content"] == "Привет20"

    finally:
        await database.close()

@pytest.mark.anyio
async def test_users_have_separate_history():
    database = Database()
    await database.connect()

    try:
        await database.clear_history(1)
        await database.clear_history(2)

        memory_service = MemoryService(database)

        await memory_service.add_message(1, "user", "Привет от первого")
        await memory_service.add_message(2, "user", "Привет от второго")

        user_1_messages = await memory_service.get_messages(1)
        user_2_messages = await memory_service.get_messages(2)

        assert user_1_messages == [
            {"role": "user", "content": "Привет от первого"}
        ]

        assert user_2_messages == [
            {"role": "user", "content": "Привет от второго"}
        ]

    finally:
        await database.close()

@pytest.mark.anyio
async def test_clear_history():
    database = Database()
    await database.connect()
    user_id = 123

    try:
        memory_service = MemoryService(database)

        await memory_service.add_message(user_id, "user", "Привет")
        await memory_service.add_message(user_id, "assistant", "Здравствуйте!")

        await memory_service.clear_history(user_id)
        messages = await memory_service.get_messages(user_id)

        assert messages == []

    finally:
        await database.close()
