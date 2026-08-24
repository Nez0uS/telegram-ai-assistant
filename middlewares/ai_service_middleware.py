from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from services import AIService


class AIServiceMiddleware(BaseMiddleware):

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data["ai_service"] = self.ai_service

        result = await handler(event, data)
        return result
