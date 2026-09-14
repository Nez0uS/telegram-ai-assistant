from config import MAX_HISTORY
from database.message_repository import MessageRepository


class MessageService:
    """
    Service for managing message history.

    :param repository: Message repository instance.

    Methods:
        add_message: Add a message to the database.
        get_messages: Get all messages from the database.
        clear_history: clear all messages from the database.
    """

    def __init__(self, repository: MessageRepository) -> None:
        self.repository = repository

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        """Add a message to the database"""
        await self.repository.create_message(user_id, role, content)

    async def get_messages(self, user_id: int) -> list[dict[str, str]]:
        """Get message history from the database"""
        return await self.repository.get_messages(user_id, MAX_HISTORY)

    async def clear_history(self, user_id: int) -> None:
        """Clear all messages from the database"""
        await self.repository.delete_messages(user_id)
