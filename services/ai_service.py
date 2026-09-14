from typing import cast

from openai import APIConnectionError, APIStatusError, AsyncOpenAI, RateLimitError
from openai.types.chat import ChatCompletionMessageParam

from config import MODEL_NAME, OPENROUTER_API_KEY
from prompts.system_prompt import SYSTEM_PROMPT

from .exceptions import AIConnectionError, AIProviderError, AIRateLimitError


class AIService:
    """
    AI service for interacting with the OpenRouter API.

    Methods:
    - get_answer: Get an answer from the AI.
    """

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY
        )
        self.model = MODEL_NAME

    async def get_answer(self, messages: list[dict[str, str]]) -> str:
        """Generate an AI response based on the conversation history"""
        try:
            request_messages = cast(
                list[ChatCompletionMessageParam],
                [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            )

            completion = await self.client.chat.completions.create(
                messages=request_messages,
                model=self.model,
            )

            content = completion.choices[0].message.content

            if content is None:
                raise AIProviderError("AI не вернул ответ.")

            return content

        except RateLimitError as error:
            raise AIRateLimitError("Слишком много запросов.") from error

        except APIStatusError as error:
            raise AIProviderError("Произошла ошибка при загрузке ответа.") from error

        except APIConnectionError as error:
            raise AIConnectionError("Ошибка подключения.") from error
