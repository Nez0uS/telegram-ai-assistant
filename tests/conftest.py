import pytest

from database import Database, MessageRepository, UserRepository


@pytest.fixture
async def database():
    database = Database()
    await database.connect()

    yield database

    await database.close()


@pytest.fixture
async def message_repository(database):
    return MessageRepository(database.pool)


@pytest.fixture
async def user_repository(database):
    return UserRepository(database.pool)
