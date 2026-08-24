import logging
from aiogram import F, Router
from aiogram.types import Message

from services import AIService, MemoryService, AIConnectionError, AIRateLimitError, AIProviderError

logger = logging.getLogger(__name__)

chat_router = Router()

@chat_router.message(F.text & ~(F.text.startswith("/")))
async def chat_handler(message: Message, memory: MemoryService, ai_service: AIService):
    try:
        user_id = message.from_user.id
        messages = await memory.get_messages(user_id)
        messages = [
            *messages,
            {
                "role": "user",
                "content": message.text
            }
        ]

        answer = await ai_service.get_answer(messages)

        await memory.add_message(
            user_id=user_id,
            role="user",
            content=message.text
        )

        await memory.add_message(
            user_id=user_id,
            role="assistant",
            content=answer
        )

        await message.answer(
            answer
        )

    except AIConnectionError:
        logger.error("Нет соединения с AI.")
        await message.answer(
            "Нет соединения с AI."
        )

    except AIRateLimitError:
        logger.warning("Слишком много запросов.")
        await message.answer(
            "Слишком много запросов."
        )

    except AIProviderError:
        logger.error("Произошла ошибка при загрузке ответа.")
        await message.answer(
            "Произошла ошибка при загрузке ответа."
        )

    except Exception:
        logger.exception("Ошибка при обработке сообщения")
        await message.answer(
            "Произошла ошибка."
        )
