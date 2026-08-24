from unittest.mock import AsyncMock, Mock
import pytest
from openai import RateLimitError

from services import AIService, AIRateLimitError


@pytest.mark.anyio
async def test_ai_service_rate_limit_error():
    ai_service = AIService()
    mock_response = Mock()

    ai_service.client.chat.completions.create = AsyncMock(
        side_effect=RateLimitError(
            message="Limit hit",
            response=mock_response,
            body=None
        )
    )

    with pytest.raises(AIRateLimitError) as exc_info:
        await ai_service.get_answer([{"role": "user", "content": "Привет"}])

    assert str(exc_info.value) == "Слишком много запросов."
