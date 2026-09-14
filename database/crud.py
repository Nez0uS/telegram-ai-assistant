from typing import Any

import asyncpg


class BaseRepository:
    """
    Base repository for common database operations.

    :param pool: asyncpg connection pool.
    :param table_name: name of the database table.

    Methods:
    - create: Create a new record.
    - get: Retrieve data from the database.
    - get_all: Retrieve all data from the database.
    - update: Update an existing record.
    - delete: Delete an existing record.
    """
    def __init__(self, pool: asyncpg.Pool, table_name: str) -> None:
        self.pool = pool
        self.table_name = table_name

    async def create(self, **kwargs: Any) -> asyncpg.Record | None:
        """
        Create a new record.

        :param kwargs: Record fields and their values.

        :return: The created record.
        """
        if not kwargs:
            raise ValueError("No fields provided")

        fields = ", ".join(kwargs.keys())
        values = list(kwargs.values())
        placeholders = ", ".join(f"${index}" for index in range(1, len(values) + 1))

        query = f"""
            INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})
            RETURNING *;
        """
        return await self.pool.fetchrow(query, *values)

    async def get(self, **kwargs: Any) -> asyncpg.Record | None:
        """
        Retrieve a single record from the database.

        :param kwargs: Fields and values used to find the record.

        :return: The retrieved record, or None if no record was found.
        """
        if not kwargs:
            raise ValueError("No fields provided")

        conditions = []
        values = list(kwargs.values())

        for index, key in enumerate(kwargs.keys(), start=1):
            conditions.append(f"{key} = ${index}")

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT * FROM {self.table_name} 
            WHERE {where_clause}
            LIMIT 1;
        """

        return await self.pool.fetchrow(query, *values)

    async def get_all(self, **kwargs: Any) -> list[asyncpg.Record]:
        """
        Retrieve all records matching the given fields and values.

        :param kwargs: Fields and values used to filter records.

        :return: A list of retrieved records.
        """
        conditions = []
        values = list(kwargs.values())

        if kwargs:
            for index, key in enumerate(kwargs.keys(), start=1):
                conditions.append(f"{key} = ${index}")

            where_clause = " AND ".join(conditions)

            query = f"""
                SELECT * FROM {self.table_name} 
                WHERE {where_clause}
            """

        else:
            query = f"""
                SELECT * FROM {self.table_name}
            """

        return await self.pool.fetch(query, *values)

    async def update(
        self, filters: dict[str, Any], **kwargs: Any
    ) -> asyncpg.Record | None:
        """
        Update an existing record based on the given filters.

        :param filters: Fields and values used to find the record.
        :param kwargs: Fields and values to update.

        :return: The updated record, or None if no record was found.
        """
        if not filters:
            raise ValueError("No fields provided")

        if not kwargs:
            raise ValueError("No fields to update")

        set_fields = []
        set_values = list(kwargs.values())
        filter_values = list(filters.values())

        for index, key in enumerate(kwargs.keys(), start=1):
            set_fields.append(f"{key} = ${index}")

        set_clause = ", ".join(set_fields)

        filter_fields = []

        for index, key in enumerate(filters.keys(), start=len(kwargs) + 1):
            filter_fields.append(f"{key} = ${index}")

        where_clause = " AND ".join(filter_fields)
        values = set_values + filter_values

        query = f"""
            UPDATE {self.table_name}
            SET {set_clause}
            WHERE {where_clause}
            RETURNING *;
        """

        return await self.pool.fetchrow(query, *values)

    async def delete(self, **kwargs: Any) -> asyncpg.Record | None:
        """
        Delete a record from the database.

        :param kwargs: Fields and values used to find the record.

        :return: The deleted record, or None if no record was found.
        """
        if not kwargs:
            raise ValueError("No fields provided")

        conditions = []
        values = list(kwargs.values())

        for index, key in enumerate(kwargs.keys(), start=1):
            conditions.append(f"{key} = ${index}")

        where_clause = " AND ".join(conditions)

        query = f"""
            DELETE FROM {self.table_name}
            WHERE {where_clause}
            RETURNING *;
        """

        return await self.pool.fetchrow(query, *values)
