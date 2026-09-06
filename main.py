import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from config.bot_commands import set_bot_commands
from config.logger import setup_logger
from database import Database, MessageRepository, UserRepository
from handlers import chat_router, clear_router, start_router
from middlewares import (
    AIServiceMiddleware,
    MemoryMiddleware,
    UserRegistrationMiddleware,
    UserServiceMiddleware,
)
from services import AIService, MemoryService, UserService

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logger = logging.getLogger(__name__)

dp.include_router(start_router)
dp.include_router(clear_router)
dp.include_router(chat_router)


async def main() -> None:
    setup_logger()

    async with Database() as database:
        message_repository = MessageRepository(database.connection_pool)
        user_repository = UserRepository(database.connection_pool)

        ai_service = AIService()
        memory = MemoryService(message_repository)
        user_service = UserService(user_repository)

        memory_middleware = MemoryMiddleware(memory)
        ai_service_middleware = AIServiceMiddleware(ai_service)
        user_service_middleware = UserServiceMiddleware(user_service)
        user_registration_middleware = UserRegistrationMiddleware(user_service)

        dp.message.outer_middleware(user_registration_middleware)
        dp.message.outer_middleware(user_service_middleware)
        dp.message.outer_middleware(memory_middleware)
        dp.message.outer_middleware(ai_service_middleware)

        await set_bot_commands(bot)

        logger.info("Ассистент запущен!")
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
