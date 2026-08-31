from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="start",
            description="Запустить ассистента"
        ),
        BotCommand(
            command="clear",
            description="Очистить историю диалога"
        )
    ]

    await bot.set_my_commands(commands)