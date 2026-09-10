from database import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, pool):
        super().__init__(pool, "users")

    async def create_user(self, telegram_id: int, name: str) -> None:
        await self.create(telegram_id=telegram_id, name=name)

    async def get_user(self, telegram_id: int) -> dict | None:
        user = await self.get(telegram_id=telegram_id)
        return dict(user) if user else None

    async def delete_user(self, telegram_id: int) -> None:
        await self.delete(telegram_id=telegram_id)
