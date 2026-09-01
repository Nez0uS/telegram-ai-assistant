from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services import UserService


start_router = Router()

@start_router.message(Command("start"))
async def start_handler(
        message: Message,
        user_service: UserService
) -> None:
    telegram_id = message.from_user.id
    name = message.from_user.first_name

    await user_service.register_user(
        telegram_id=telegram_id,
        name=name
    )
    await message.answer("Привет! Я AI-ассистент.")
