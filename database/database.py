from typing import Self

import asyncpg

from config import DATABASE_URL


class Database:
    """Manage the PostgreSQL connection pool."""
    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    @property
    def connection_pool(self) -> asyncpg.Pool:
        """Return the active database connection pool."""
        if self.pool is None:
            raise RuntimeError("Database is not connected")

        return self.pool

    async def connect(self) -> None:
        """Create a PostgreSQL connection pool."""
        self.pool = await asyncpg.create_pool(DATABASE_URL)

    async def close(self) -> None:
        """Close the PostgreSQL connection pool."""
        if self.pool is not None:
            await self.pool.close()

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()
