import asyncpg

from config import DATABASE_URL


class Database:

    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def create_tables(self):
        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS messages (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)

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
