import asyncio

from aiogram import Bot, Dispatcher

from handlers import start_router, chat_router
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(chat_router)


async def main():
    print("Ассистент запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())