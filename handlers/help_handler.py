from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()


@help_router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n\n"
        "/start — запустить бота\n"
        "/help — показать справку\n"
        "/clear — очистить историю диалога\n\n"
        "Просто отправь сообщение, чтобы начать общение с AI."
    )
