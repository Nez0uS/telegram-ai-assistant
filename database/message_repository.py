import asyncpg

from database import BaseRepository


class MessageRepository(BaseRepository):
    def __init__(self, pool: asyncpg.Pool):
        super().__init__(pool, "messages")

    async def create_message(self, user_id: int, role: str, content: str) -> None:
        await self.create(user_id=user_id, role=role, content=content)

    async def get_messages(self, user_id: int, limit: int) -> list[dict[str, str]]:
        messages = await self.pool.fetch(
            """
            SELECT role, content 
            FROM messages 
            WHERE user_id = $1 
            ORDER BY created_at DESC 
            LIMIT $2
            """,
            user_id,
            limit,
        )

        messages.reverse()

        return [dict(message) for message in messages]

    async def delete_messages(self, user_id: int) -> None:
        await self.pool.execute(
            """
            DELETE FROM messages 
            WHERE user_id = $1
            """,
            user_id,
        )
