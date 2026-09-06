from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from services import AIService


class AIServiceMiddleware(BaseMiddleware):
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["ai_service"] = self.ai_service

        return await handler(event, data)
