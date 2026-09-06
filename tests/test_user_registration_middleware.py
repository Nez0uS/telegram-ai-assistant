from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.types import Chat, Message, User

from middlewares import UserRegistrationMiddleware


@pytest.mark.anyio
async def test_user_registration_middleware():
    user_service = Mock()
    user_service.register_user = AsyncMock()

    middleware = UserRegistrationMiddleware(user_service)

    user = User(
        id=12345,
        is_bot=False,
        first_name="Name",
        last_name=None,
        username=None,
        language_code=None,
    )

    event = Message(
        message_id=1,
        date=datetime.now(timezone.utc),
        chat=Chat(id=1, type="private"),
        from_user=user,
    )

    handler = AsyncMock()
    data = {}

    await middleware(handler, event, data)

    user_service.register_user.assert_awaited_once_with(12345, "Name")

    handler.assert_awaited_once()
