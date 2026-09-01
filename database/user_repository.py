class UserRepository:

    def __init__(self, pool):
        self.pool = pool

    async def create_user(
            self,
            telegram_id: int,
            name: str
    ) -> None:
        await self.pool.execute(
            """
            INSERT INTO users (telegram_id, name)
            VALUES ($1, $2)
            """,
            telegram_id,
            name
        )

    async def get_user(
            self,
            telegram_id: int
    ) -> dict | None:
        user = await self.pool.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1",
            telegram_id
        )

        return dict(user) if user else None
