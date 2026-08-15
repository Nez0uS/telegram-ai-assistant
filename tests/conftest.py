import pytest

from database import Database


@pytest.fixture
async def database():
    database = Database()
    await database.connect()

    yield database

    await database.close()

