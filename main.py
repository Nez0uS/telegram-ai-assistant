import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.logger import setup_logger
from database import Database, MessageRepository
from handlers import start_router, chat_router, clear_router
from config import BOT_TOKEN
from config.bot_commands import set_bot_commands
from services import MemoryService, AIService
from middlewares import MemoryMiddleware, AIServiceMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
database = Database()
logger = logging.getLogger(__name__)

dp.include_router(start_router)
dp.include_router(clear_router)
dp.include_router(chat_router)


async def main() -> None:
    setup_logger()

    try:
        await database.connect()

        repository = MessageRepository(database.pool)
        ai_service = AIService()
        memory = MemoryService(repository)

        memory_middleware = MemoryMiddleware(memory)
        ai_service_middleware = AIServiceMiddleware(ai_service)

        dp.message.outer_middleware(memory_middleware)
        dp.message.outer_middleware(ai_service_middleware)

        await set_bot_commands(bot)

        logger.info("Ассистент запущен!")
        await dp.start_polling(bot)

    finally:
        logger.info("Завершение работы...")
        await database.close()


if __name__ == "__main__":
    asyncio.run(main())