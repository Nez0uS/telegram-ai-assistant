from database import UserRepository


class UserService:
    """
    Service for managing users.

    :param repository: User repository instance.

    Methods:
        register_user: Add a user to the database.
        get_user: Get user from the database.
        delete_user: Delete a user from the database.
        get_user_id: Get the user ID from the database.
    """

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register_user(self, telegram_id: int, name: str) -> None:
        """Add a user to the database"""
        user = await self.get_user(telegram_id)
        if user is None:
            await self.repository.create_user(telegram_id, name)

    async def get_user(self, telegram_id: int) -> dict | None:
        """Get a user from the database"""
        return await self.repository.get_user(telegram_id)

    async def delete_user(self, telegram_id: int) -> None:
        """Delete a user from the database"""
        await self.repository.delete_user(telegram_id)

    async def get_user_id(self, telegram_id: int) -> int | None:
        """Get a user id from the database"""
        user = await self.repository.get_user(telegram_id)

        if user is None:
            return None

        return user["id"]
