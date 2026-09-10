import logging

from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from services import (
    AIConnectionError,
    AIProviderError,
    AIRateLimitError,
    AIService,
    MemoryService,
    UserService,
)

logger = logging.getLogger(__name__)

chat_router = Router()


@chat_router.message(F.text & ~(F.text.startswith("/")))
async def chat_handler(
    message: Message,
    memory: MemoryService,
    ai_service: AIService,
    user_service: UserService,
):
    try:
        if message.from_user is None:
            return

        telegram_id = message.from_user.id

        user_id = await user_service.get_user_id(telegram_id)

        if user_id is None:
            await message.answer("Пользователь не найден!")
            return

        text = message.text
        if text is None:
            return

        messages = await memory.get_messages(user_id)
        messages = [*messages, {"role": "user", "content": text}]

        if message.bot is None:
            return

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            answer = await ai_service.get_answer(messages)

        await memory.add_message(user_id=user_id, role="user", content=text)

        await memory.add_message(user_id=user_id, role="assistant", content=answer)

        await message.answer(answer)

    except AIConnectionError:
        logger.error("Нет соединения с AI.")
        await message.answer("Нет соединения с AI.")

    except AIRateLimitError:
        logger.warning("Слишком много запросов.")
        await message.answer("Слишком много запросов.")

    except AIProviderError:
        logger.error("Произошла ошибка при загрузке ответа.")
        await message.answer("Произошла ошибка при загрузке ответа.")

    except Exception:
        logger.exception("Ошибка при обработке сообщения")
        await message.answer("Произошла ошибка.")
