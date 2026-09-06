from typing import Self

import asyncpg

from config import DATABASE_URL


class Database:
    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    @property
    def connection_pool(self) -> asyncpg.Pool:
        if self.pool is None:
            raise RuntimeError("Database is not connected")

        return self.pool

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(DATABASE_URL)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()
