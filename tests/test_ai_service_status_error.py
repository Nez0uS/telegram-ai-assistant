from unittest.mock import AsyncMock, Mock
import pytest
from openai import APIStatusError

from services import AIService, AIProviderError


@pytest.mark.anyio
async def test_ai_service_status_error():
    ai_service = AIService()
    mock_response = Mock()

    ai_service.client.chat.completions.create = AsyncMock(
        side_effect=APIStatusError(
            message="Ошибка статуса.",
            response=mock_response,
            body=None
        )
    )

    with pytest.raises(AIProviderError) as exc_info:
        await ai_service.get_answer([{"role": "user", "content": "Привет"}])

    assert str(exc_info.value) == "Произошла ошибка при загрузке ответа."
