from unittest.mock import AsyncMock, Mock
import pytest

from PROMPTS import PROMPT1
from config import MODEL_NAME
from services import AIService


@pytest.mark.anyio
async def test_ai_service():
    message = Mock()
    message.content = "Привет!"

    choice = Mock()
    choice.message = message

    completion = Mock()
    completion.choices = [choice]

    ai_service = AIService()
    ai_service.client.chat.completions.create = AsyncMock(return_value=completion)

    result = await ai_service.get_answer([{"role": "user", "content": "Привет!"}])

    assert result == "Привет!"

    ai_service.client.chat.completions.create.assert_awaited_once_with(
        messages=[
            {"role": "system", "content": PROMPT1},
            {"role": "user", "content": "Привет!"}
        ],
        model=MODEL_NAME
    )
