import logging
from aiogram import F, Router
from aiogram.types import Message
from openai import APIConnectionError, RateLimitError, APIStatusError

from services import AIService, MemoryService

logger = logging.getLogger(__name__)
ai_service = AIService()
chat_router = Router()

@chat_router.message(F.text & ~(F.text.startswith("/")))
async def chat_handler(message: Message, memory: MemoryService):
    try:
        user_id = message.from_user.id

        await memory.add_message(user_id=user_id, role="user", content=message.text)
        messages = await memory.get_messages(user_id)
        answer = await ai_service.get_answer(messages)
        await memory.add_message(user_id=user_id, role="assistant", content=answer)
        await message.answer(
            answer
        )

    except APIConnectionError:
        logger.error("Нет соединения с AI.")
        await message.answer(
            "Нет соединения с AI."
        )

    except RateLimitError:
        logger.warning("Слишком много запросов.")
        await message.answer(
            "Слишком много запросов."
        )

    except APIStatusError:
        logger.error("Произошла ошибка при загрузке ответа.")
        await message.answer(
            "Произошла ошибка при загрузке ответа."
        )

    except ValueError:
        logger.error("AI не смог сформировать ответ.")
        await message.answer(
            "AI не смог сформировать ответ."
        )

    except Exception:
        logger.exception("Ошибка при обработке сообщения")
        await message.answer(
            "Произошла ошибка."
        )
