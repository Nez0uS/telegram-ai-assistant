from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot) -> None:
    """Configure the bot command menu"""
    commands = [
        BotCommand(command="start", description="Запустить ассистента"),
        BotCommand(command="clear", description="Очистить историю диалога"),
        BotCommand(command="help", description="Руководство по командам"),
    ]

    await bot.set_my_commands(commands)
