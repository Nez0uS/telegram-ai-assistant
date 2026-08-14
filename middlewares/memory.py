from aiogram import BaseMiddleware
from services import MemoryService
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable


class MemoryMiddleware(BaseMiddleware):

    def __init__(self, memory: MemoryService):
        self.memory = memory

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data["memory"] = self.memory

        result = await handler(event, data)
        return result