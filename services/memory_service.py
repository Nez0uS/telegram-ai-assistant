from config import MAX_HISTORY
from database.message_repository import MessageRepository


class MemoryService:
    def __init__(self, repository: MessageRepository) -> None:
        self.repository = repository

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        await self.repository.create_message(user_id, role, content)

    async def get_messages(self, user_id: int) -> list[dict[str, str]]:
        return await self.repository.get_messages(user_id, MAX_HISTORY)

    async def clear_history(self, user_id: int) -> None:
        await self.repository.delete_messages(user_id)
