from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from services import MessageService


class MessageMiddleware(BaseMiddleware):
    """Middleware that provides MessageService to handlers"""

    def __init__(self, memory: MessageService) -> None:
        self.memory = memory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Inject MessageService into handler data"""
        data["memory"] = self.memory

        return await handler(event, data)
