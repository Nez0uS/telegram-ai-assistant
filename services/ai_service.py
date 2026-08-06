from openai import AsyncOpenAI

from PROMPTS import PROMPT1
from config import OPENROUTER_API_KEY, MODEL_NAME


class AIService:

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
        self.model = MODEL_NAME

    async def get_answer(self, text: str) -> str:

        completion = await self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": PROMPT1
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model=self.model,
        )

        content = completion.choices[0].message.content

        if content is None:
            raise ValueError("Модель не вернула ответ.")

        return content
