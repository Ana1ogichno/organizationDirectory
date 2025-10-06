from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
)

from src.client.interfaces import IPostgresSessionProvider
from src.client.storages.postgres.interfaces import (
    IPostgresEngine,
    IPostgresSessionContextManager,
)


class PostgresSessionProvider(IPostgresSessionProvider):
    """
    PostgresSessionProvider is responsible for providing PostgreSQL database sessions.

    This class implements the IPostgresSessionProvider interface. It provides methods
    to create and return asynchronous sessions to interact with the PostgreSQL database.
    """

    def __init__(
        self,
        psql_engine: IPostgresEngine,
        context_manager: IPostgresSessionContextManager,
    ):
        """
        Initialize the PostgresSessionProvider with an async session factory and
        context manager.

        :param psql_engine: Interface for async SQLAlchemy engine.
        :param context_manager: Context manager implementing
                IPostgresSessionContextManager.
        """

        self._session_factory = async_sessionmaker(
            bind=psql_engine.get(),
            autocommit=False,
            autoflush=False,
        )
        self._context_manager = context_manager

    def get_session(self) -> async_scoped_session[AsyncSession]:
        """
        Creates and returns a new asynchronous session for PostgreSQL.

        :return: A new AsyncSession instance for PostgreSQL.
        """

        return async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=self._context_manager.get_session_context,
        )
