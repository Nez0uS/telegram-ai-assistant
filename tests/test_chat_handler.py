from unittest.mock import AsyncMock, Mock
import pytest

from handlers import chat_handler


@pytest.mark.anyio
async def test_chat_handler():
    message = Mock()
    memory = Mock()
    ai_service = Mock()

    message.from_user.id = 123
    message.text = "Как дела?"
    message.answer = AsyncMock()

    memory.get_messages = AsyncMock(
        return_value=[
            {"role": "user", "content": "Привет"}
        ]
    )

    memory.add_message = AsyncMock()

    ai_service.get_answer = AsyncMock(
        return_value="Хорошо! У меня всё отлично."
    )

    await chat_handler.chat_handler(message, memory, ai_service)

    memory.get_messages.assert_awaited_once_with(123)

    ai_service.get_answer.assert_awaited_once_with(
        [
            {"role": "user", "content": "Привет"},
            {"role": "user", "content": "Как дела?"}
        ]
    )

    memory.add_message.assert_any_await(
        user_id=123,
        role="user",
        content="Как дела?"
    )

    memory.add_message.assert_any_await(
        user_id=123,
        role="assistant",
        content="Хорошо! У меня всё отлично."
    )

    message.answer.assert_awaited_once_with(
        "Хорошо! У меня всё отлично."
    )
