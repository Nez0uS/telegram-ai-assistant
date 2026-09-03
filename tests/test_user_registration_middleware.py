from unittest.mock import AsyncMock, Mock
import pytest

from middlewares import UserRegistrationMiddleware


@pytest.mark.anyio
async def test_user_registration_middleware():
    user_service = Mock()
    user_service.register_user = AsyncMock()

    middleware = UserRegistrationMiddleware(user_service)

    event = Mock()
    event.from_user.id = 12345
    event.from_user.first_name = "Name"

    handler = AsyncMock()
    data = {}

    await middleware(handler, event, data)

    user_service.register_user.assert_awaited_once_with(12345, "Name")

    handler.assert_awaited_once()
