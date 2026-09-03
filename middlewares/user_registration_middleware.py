from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from services import UserService


class UserRegistrationMiddleware(BaseMiddleware):

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        telegram_id = event.from_user.id
        name = event.from_user.first_name

        await self.user_service.register_user(telegram_id, name)

        result = await handler(event, data)
        return result
