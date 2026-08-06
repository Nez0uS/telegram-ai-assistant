from aiogram import Router
from aiogram.types import Message
from openai import APIConnectionError, RateLimitError, APIStatusError

from services import AIService

ai_service = AIService()
chat_router = Router()

@chat_router.message()
async def chat_handler(message: Message):
    try:
        answer = await ai_service.get_answer(message.text)
        await message.answer(
            answer
        )

    except APIConnectionError:
        await message.answer(
            "Нет соединения с AI."
        )

    except RateLimitError:
        await message.answer(
            "Слишком много запросов."
        )

    except APIStatusError:
        await message.answer(
            "Произошла ошибка при загрузке ответа."
        )

    except ValueError:
        await message.answer(
            "AI не смог сформировать ответ."
        )

    except Exception as e:
        print(e)
        await message.answer(
            "Произошла ошибка."
        )