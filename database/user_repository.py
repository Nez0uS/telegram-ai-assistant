import asyncpg

from database import BaseRepository


class UserRepository(BaseRepository):
    """User repository for operations on the users table"""

    def __init__(self, pool: asyncpg.Pool) -> None:
        super().__init__(pool, "users")

    async def create_user(self, telegram_id: int, name: str) -> None:
        """Create a new user record in the users table"""
        await self.create(telegram_id=telegram_id, name=name)

    async def get_user(self, telegram_id: int) -> dict | None:
        """Retrieve a user using telegram_id"""
        user = await self.get(telegram_id=telegram_id)
        return dict(user) if user else None

    async def delete_user(self, telegram_id: int) -> None:
        """Delete a user using telegram_id"""
        await self.delete(telegram_id=telegram_id)
