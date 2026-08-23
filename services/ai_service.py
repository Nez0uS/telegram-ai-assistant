from openai import AsyncOpenAI, RateLimitError, APIStatusError, APIConnectionError

from PROMPTS import PROMPT1
from config import OPENROUTER_API_KEY, MODEL_NAME
from .exceptions import AIConnectionError, AIProviderError, AIRateLimitError


class AIService:

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
        self.model = MODEL_NAME

    async def get_answer(self, messages: list[dict[str, str]]) -> str:
        try:
            request_messages = [
                {"role": "system", "content": PROMPT1}
            ] + messages

            completion = await self.client.chat.completions.create(
                messages=request_messages,
                model=self.model,
            )

            content = completion.choices[0].message.content

            return content

        except RateLimitError as error:
            raise AIRateLimitError("Ошибка лимита скорости.") from error

        except APIStatusError as error:
            raise AIProviderError("Ошибка статуса.") from error

        except APIConnectionError as error:
            raise AIConnectionError("Ошибка подключения.") from error
