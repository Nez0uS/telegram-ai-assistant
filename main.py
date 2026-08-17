import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.logger import setup_logger
from database import Database, MessageRepository
from handlers import start_router, chat_router, clear_router
from config import BOT_TOKEN
from services import MemoryService
from middlewares import MemoryMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
database = Database()
logger = logging.getLogger(__name__)

dp.include_router(start_router)
dp.include_router(clear_router)
dp.include_router(chat_router)


async def main():
    setup_logger()

    try:
        await database.connect()

        repository = MessageRepository(database.pool)

        memory = MemoryService(repository)
        memory_middleware = MemoryMiddleware(memory)
        dp.message.outer_middleware(memory_middleware)

        logger.info("Ассистент запущен!")
        await dp.start_polling(bot)

    finally:
        logger.info("Завершение работы...")
        await database.close()


if __name__ == "__main__":
    asyncio.run(main())