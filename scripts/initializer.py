import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import logging

from src.client.storages.deps import get_db, get_postgres_session_provider
from src.client.storages.postgres.core import PostgresSessionContextManager
from src.client.storages.postgres.init.deps import get_psql_initializer


class DatabasesInitializer:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @staticmethod
    async def _init_psql() -> None:
        """Initialize PostgreSQL database"""

        id_context = random.randint(1, 100000)  # noqa: S311

        PostgresSessionContextManager.set_session_context(id_context)

        session_provider = get_postgres_session_provider()

        async for db in get_db(session_provider=session_provider):
            psql_initializer = await get_psql_initializer(db=db)

            await psql_initializer.init()

        PostgresSessionContextManager.remove_session_context()

    async def _initialize(self) -> None:
        """Main initialization method"""

        self._logger.info("Initial PostgreSql")
        await self._init_psql()
        self._logger.info("End initial PostgreSql")

    @classmethod
    async def run(cls) -> None:
        """Class method to run the initialization"""
        initializer = cls()
        await initializer._initialize()


if __name__ == "__main__":
    asyncio.run(DatabasesInitializer.run())
