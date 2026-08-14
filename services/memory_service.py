from database import Database


class MemoryService:

    MAX_HISTORY = 20

    def __init__(self, database: Database) -> None:
        self.database = database

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        await self.database.insert_message(user_id, role, content)

    async def get_messages(self, user_id: int) -> list[dict[str, str]]:
        return await self.database.get_messages(user_id, self.MAX_HISTORY)

    async def clear_history(self, user_id: int) -> None:
        await self.database.clear_history(user_id)
