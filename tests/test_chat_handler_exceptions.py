from unittest.mock import Mock, AsyncMock
import pytest
from services import AIConnectionError, AIRateLimitError, AIProviderError

from handlers import chat_handler


@pytest.mark.anyio
async def test_chat_handler_connection_error():
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

    ai_service.get_answer = AsyncMock(side_effect=AIConnectionError())

    await chat_handler.chat_handler(message, memory, ai_service)
    memory.add_message.assert_not_awaited()

    message.answer.assert_awaited_once_with(
        "Нет соединения с AI."
    )

@pytest.mark.anyio
async def test_chat_handler_rate_limit_error():
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

    ai_service.get_answer = AsyncMock(side_effect=AIRateLimitError())

    await chat_handler.chat_handler(message, memory, ai_service)
    memory.add_message.assert_not_awaited()

    message.answer.assert_awaited_once_with(
        "Слишком много запросов."
    )

@pytest.mark.anyio
async def test_chat_handler_provider_error():
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

    ai_service.get_answer = AsyncMock(side_effect=AIProviderError())

    await chat_handler.chat_handler(message, memory, ai_service)
    memory.add_message.assert_not_awaited()

    message.answer.assert_awaited_once_with(
        "Произошла ошибка при загрузке ответа."
    )
