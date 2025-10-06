from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.client.storages.postgres.interfaces import IPostgresEngine
from src.config.settings.deps import get_settings


class PostgresEngine(IPostgresEngine):
    """
    Encapsulates the creation and management of an async SQLAlchemy engine for
    PostgreSQL.
    """

    def __init__(self):
        """
        Initializes the PostgresEngine with settings from the application configuration.
        """

        self._psql_engine = create_async_engine(
            url=get_settings().postgres.POSTGRES_DATABASE_URL.unicode_string(),
            pool_pre_ping=True,
            pool_size=get_settings().postgres.POOL_SIZE,
            max_overflow=0,
        )

    def get(self) -> AsyncEngine:
        """
        Retrieve the async SQLAlchemy engine.

        :return: Configured AsyncEngine instance.
        """

        return self._psql_engine
