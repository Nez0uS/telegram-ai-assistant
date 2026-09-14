from unittest.mock import AsyncMock, Mock

import pytest

from middlewares import MessageMiddleware


@pytest.mark.anyio
async def test_messages_middleware():
    messages = Mock()
    middleware = MessageMiddleware(messages)

    event = Mock()
    handler = AsyncMock()
    data = {}

    await middleware(handler, event, data)

    assert data["memory"] is messages
    handler.assert_awaited_once_with(event, data)
