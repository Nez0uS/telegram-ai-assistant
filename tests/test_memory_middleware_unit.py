from unittest.mock import AsyncMock, Mock
import pytest

from middlewares import MemoryMiddleware


@pytest.mark.anyio
async def test_memory_middleware():
    memory = Mock()
    middleware = MemoryMiddleware(memory)

    event = Mock()
    handler = AsyncMock()
    data = {}

    await middleware(handler, event, data)

    assert data["memory"] is memory
    handler.assert_awaited_once_with(event, data)
