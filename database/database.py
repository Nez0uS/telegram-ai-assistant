import asyncpg

from config import DATABASE_URL


class Database:

    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(DATABASE_URL)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
