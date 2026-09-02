from database import UserRepository


class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register_user(
        self,
        telegram_id: int,
        name: str
    ) -> None:
        user = await self.get_user(telegram_id)
        if user is None:
            await self.repository.create_user(
                telegram_id,
                name
            )

    async def get_user(
        self,
        telegram_id: int
    ) -> dict | None:
        return await self.repository.get_user(telegram_id)

    async def delete_user(
            self,
            telegram_id: int
    ) -> None:
        await self.repository.delete_user(telegram_id)
