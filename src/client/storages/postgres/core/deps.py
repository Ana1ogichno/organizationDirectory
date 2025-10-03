from src.client.storages.postgres.core import (
    PostgresEngine,
    PostgresSessionContextManager,
)
from src.client.storages.postgres.interfaces import (
    IPostgresEngine,
    IPostgresSessionContextManager,
)


def get_postgres_engine() -> IPostgresEngine:
    """
    Create and return a PostgresEngine instance implementing IPostgresEngine.

    :return: PostgresEngine instance.
    """

    return PostgresEngine()


def get_postgres_session_context_manager() -> IPostgresSessionContextManager:
    """
    Dependency provider function that returns an instance of
    PostgresSessionContextManager.

    This function is typically used in dependency injection containers (e.g., FastAPI)
    to provide a concrete implementation of IPostgresSessionContextManager wherever
    needed.

    :return: An instance of IPostgresSessionContextManager.
    """

    return PostgresSessionContextManager()
