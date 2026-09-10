import pytest

from database import BaseRepository


@pytest.fixture
async def base_repository(database):
    await database.pool.execute(
        """
        CREATE TABLE IF NOT EXISTS test_users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE NOT NULL,
        name VARCHAR(255),
        age INTEGER
        )
        """
    )

    yield BaseRepository(database.pool, "test_users")

    await database.pool.execute("DROP TABLE test_users")


@pytest.mark.anyio
async def test_create_user(base_repository: BaseRepository) -> None:
    user = await base_repository.create(telegram_id=123, name="test_user1", age=18)

    assert user is not None
    assert user["telegram_id"] == 123
    assert user["name"] == "test_user1"
    assert user["age"] == 18


@pytest.mark.anyio
async def test_get_user(base_repository: BaseRepository) -> None:
    await base_repository.create(telegram_id=123, name="test_user1", age=18)

    user = await base_repository.get(telegram_id=123)

    assert user is not None
    assert user["telegram_id"] == 123
    assert user["name"] == "test_user1"
    assert user["age"] == 18


@pytest.mark.anyio
async def test_get_all_users(base_repository: BaseRepository) -> None:
    await base_repository.create(telegram_id=111, name="test_user1", age=18)

    await base_repository.create(telegram_id=222, name="test_user2", age=19)

    users = await base_repository.get_all()
    users_by_id = {user["telegram_id"]: user for user in users}

    assert len(users) == 2

    assert users_by_id[111]["name"] == "test_user1"
    assert users_by_id[111]["age"] == 18

    assert users_by_id[222]["name"] == "test_user2"
    assert users_by_id[222]["age"] == 19


@pytest.mark.anyio
async def test_update_user(base_repository: BaseRepository) -> None:
    await base_repository.create(telegram_id=111, name="test_user1", age=18)

    await base_repository.update({"telegram_id": 111}, name="updated_name", age=20)

    user = await base_repository.get(telegram_id=111)

    assert user is not None
    assert user["name"] == "updated_name"
    assert user["age"] == 20


@pytest.mark.anyio
async def test_delete_user(base_repository: BaseRepository) -> None:
    await base_repository.create(telegram_id=111, name="test_user1", age=18)

    user_before_delete = await base_repository.get(telegram_id=111)

    assert user_before_delete is not None

    await base_repository.delete(telegram_id=111)

    user_after_delete = await base_repository.get(telegram_id=111)

    assert user_after_delete is None
