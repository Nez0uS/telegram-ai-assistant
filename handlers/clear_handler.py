from aiogram import Router

from services import MemoryService, UserService
from aiogram.types import Message
from aiogram.filters import Command


clear_router = Router()

@clear_router.message(Command("clear"))
async def clear_handler(
    message: Message,
    memory: MemoryService,
    user_service: UserService
) -> None:
    telegram_id = message.from_user.id

    user = await user_service.get_user(telegram_id)
    user_id = user["id"]

    await memory.clear_history(user_id)
    await message.answer("История успешно удалена!")