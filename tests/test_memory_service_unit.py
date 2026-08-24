from unittest.mock import AsyncMock, Mock
import pytest

from services import MemoryService


@pytest.mark.anyio
async def test_memory_service_add_message():
    repository = Mock()
    repository.insert_message = AsyncMock()

    memory_service = MemoryService(repository)

    await memory_service.add_message(
        123,
        "user",
        "Привет"
    )

    repository.insert_message.assert_awaited_once_with(
        123,
        "user",
        "Привет"
    )

@pytest.mark.anyio
async def test_memory_service_get_messages():
    repository = Mock()
    repository.get_messages = AsyncMock(
        return_value=[
            {"role": "user", "content": "Привет"}
        ]
    )

    memory_service = MemoryService(repository)

    result = await memory_service.get_messages(123)

    repository.get_messages.assert_awaited_once_with(123, 20)

    assert result == [
        {"role": "user", "content": "Привет"}
    ]

@pytest.mark.anyio
async def test_memory_service_clear_history():
    repository = Mock()
    repository.clear_history = AsyncMock()

    memory_service = MemoryService(repository)

    result = await memory_service.clear_history(123)
    repository.clear_history.assert_awaited_once_with(123)

    assert result is None
