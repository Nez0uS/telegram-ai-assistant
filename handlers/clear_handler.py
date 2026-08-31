from aiogram import Router

from services import MemoryService
from aiogram.types import Message
from aiogram.filters import Command


clear_router = Router()


@clear_router.message(Command("clear"))
async def clear_handler(
        message: Message,
        memory: MemoryService
) -> None:
    user_id = message.from_user.id

    await memory.clear_history(user_id)
    await message.answer("История успешно удалена!")