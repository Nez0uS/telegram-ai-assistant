import asyncio

from aiogram import Bot, Dispatcher

from database import Database
from handlers import start_router, chat_router
from config import BOT_TOKEN
from services import MemoryService
from middlewares import MemoryMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
database = Database()

dp.include_router(start_router)
dp.include_router(chat_router)


async def main():
    await database.connect()

    memory = MemoryService(database)
    memory_middleware = MemoryMiddleware(memory)
    chat_router.message.outer_middleware(memory_middleware)

    try:
        print("Ассистент запущен")
        await dp.start_polling(bot)

    finally:
        await database.close()


if __name__ == "__main__":
    asyncio.run(main())