from aiogram import Router
from aiogram.types import Message
from openai import APIConnectionError, RateLimitError, APIStatusError

from services import AIService, MemoryService


ai_service = AIService()
chat_router = Router()

@chat_router.message()
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

    except APIConnectionError as e:
        print(e)
        await message.answer(
            "Нет соединения с AI."
        )

    except RateLimitError as e:
        print(e)
        await message.answer(
            "Слишком много запросов."
        )

    except APIStatusError as e:
        print(e)
        await message.answer(
            "Произошла ошибка при загрузке ответа."
        )

    except ValueError as e:
        print(e)
        await message.answer(
            "AI не смог сформировать ответ."
        )

    except Exception as e:
        print(e)
        await message.answer(
            "Произошла ошибка."
        )
