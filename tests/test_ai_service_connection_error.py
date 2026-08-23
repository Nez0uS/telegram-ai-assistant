from unittest.mock import AsyncMock, Mock
import pytest
from openai import APIConnectionError

from services import AIService, AIConnectionError


@pytest.mark.anyio
async def test_ai_service_connection_error():
    ai_service = AIService()
    mock_request = Mock()

    ai_service.client.chat.completions.create = AsyncMock(
        side_effect=APIConnectionError(
            message="Connection error.",
            request=mock_request
        )
    )

    with pytest.raises(AIConnectionError) as exc_info:
        await ai_service.get_answer([{"role": "user", "content": "Привет"}])

    assert str(exc_info.value) == "Ошибка подключения."
