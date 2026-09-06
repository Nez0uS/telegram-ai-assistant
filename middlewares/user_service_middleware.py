from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from services import UserService


class UserServiceMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["user_service"] = self.user_service

        return await handler(event, data)
