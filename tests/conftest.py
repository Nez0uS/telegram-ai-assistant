import pytest

from database import Database, MessageRepository


@pytest.fixture
async def database():
    database = Database()
    await database.connect()

    yield database

    await database.close()

@pytest.fixture
async def repository(database):
    return MessageRepository(database.pool)

