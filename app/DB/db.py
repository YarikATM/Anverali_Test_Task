import datetime

import asyncpg
import logging
import asyncio
import asyncpg.exceptions

logger = logging.getLogger(__name__)


class Database:

    def __init__(self, host, user, db_name, password):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = None

    async def connect(self):
        try:
            self.connection = await asyncpg.connect(
                user=self.user,
                password=self.password,
                database=self.db_name,
                host=self.host
            )

            logger.info('Database connection succeed')

        except Exception as e:
            logger.exception(f'DB error: {str(e)}')
            self.connection = None

    async def add_task(self, data):
        try:

            query = """
                    INSERT INTO tasks (title, description, expire)
                    VALUES ($1, $2, $3)
            """

            await self.connection.execute(query,
                                          data.get('title'),
                                          data.get('description'),
                                          data.get('expire'))
            logger.info(f'Task added data:{data}')

        except (asyncpg.exceptions.ConnectionDoesNotExistError, asyncpg.exceptions.ConnectionFailureError,
                asyncpg.exceptions.ClientCannotConnectError):
            await self.connection()
            await self.add_task(data)

    async def get_tasks(self):
        try:

            query = """
                    SELECT * FROM tasks
            """

            res = await self.connection.fetch(query)

            return res

        except (asyncpg.exceptions.ConnectionDoesNotExistError, asyncpg.exceptions.ConnectionFailureError,
                asyncpg.exceptions.ClientCannotConnectError):
            await self.connection()
            return await self.get_tasks()

