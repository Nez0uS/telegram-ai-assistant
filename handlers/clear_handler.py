from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services import MemoryService, UserService

clear_router = Router()


@clear_router.message(Command("clear"))
async def clear_handler(
    message: Message, memory: MemoryService, user_service: UserService
) -> None:

    if message.from_user is None:
        return

    telegram_id = message.from_user.id

    user = await user_service.get_user(telegram_id)

    if user is None:
        await message.answer("Пользователь не найден!")
        return

    user_id = user["id"]

    await memory.clear_history(user_id)
    await message.answer("История успешно удалена!")
