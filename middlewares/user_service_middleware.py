from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from services import UserService


class UserServiceMiddleware(BaseMiddleware):

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data["user_service"] = self.user_service

        result = await handler(event, data)
        return result
