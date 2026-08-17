import asyncpg


class MessageRepository:

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def insert_message(
            self,
            user_id: int,
            role: str,
            content: str
    ) -> None:
        await self.pool.execute("""
            INSERT INTO messages (user_id, role, content)
            VALUES ($1, $2, $3)
            """,
            user_id,
            role,
            content
        )

    async def get_messages(
            self,
            user_id: int,
            limit: int
    ) -> list[dict[str, str]]:
        rows = await self.pool.fetch(
            """
            SELECT role, content
            FROM (
                SELECT id, role, content
                FROM messages
                WHERE user_id = $1
                ORDER BY id DESC
                LIMIT $2
            ) AS recent_messages
            ORDER BY id
            """,
            user_id,
            limit
        )

        return [
            {"role": row["role"], "content": row["content"]}
            for row in rows
        ]

    async def clear_history(
            self,
            user_id: int
    ) -> None:
        await self.pool.execute(
            """
            DELETE FROM messages 
            WHERE user_id = $1
            """,
            user_id
        )