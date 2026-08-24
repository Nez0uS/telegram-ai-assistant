from unittest.mock import AsyncMock, Mock
import pytest

from middlewares import AIServiceMiddleware


@pytest.mark.anyio
async def test_ai_service_middleware():
    ai_service = Mock()
    middleware = AIServiceMiddleware(ai_service)

    event = Mock()
    handler = AsyncMock()
    data = {}

    await middleware(handler, event, data)

    assert data["ai_service"] is ai_service
    handler.assert_awaited_once_with(event, data)
