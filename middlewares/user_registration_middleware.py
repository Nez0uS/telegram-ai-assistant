from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from services import UserService


class UserRegistrationMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        if not isinstance(event, Message):
            return await handler(event, data)

        if event.from_user is None:
            return await handler(event, data)

        telegram_id = event.from_user.id
        name = event.from_user.first_name

        await self.user_service.register_user(telegram_id, name)

        return await handler(event, data)
