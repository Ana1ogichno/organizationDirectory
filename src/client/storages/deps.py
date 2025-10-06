from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from src.client.interfaces import IPostgresSessionProvider
from src.client.storages import PostgresSessionProvider
from src.client.storages.postgres.core.deps import (
    get_postgres_engine,
    get_postgres_session_context_manager,
)


def get_postgres_session_provider() -> IPostgresSessionProvider:
    """
    Construct and return an instance of IPostgresSessionProvider.

    This function initializes a PostgresSessionProvider with a session context manager,
    allowing it to provide context-aware PostgreSQL sessions. Typically used as a
    dependency provider in FastAPI or other service layers to abstract session retrieval
    logic.

    :return: An instance of IPostgresSessionProvider implementation.
    """

    return PostgresSessionProvider(
        psql_engine=get_postgres_engine(),
        context_manager=get_postgres_session_context_manager(),
    )


async def get_db(
    session_provider: Annotated[
        IPostgresSessionProvider, Depends(get_postgres_session_provider)
    ],
) -> AsyncGenerator:
    """
    Provides a PostgreSQL database session.

    This dependency can be used to inject a PostgreSQL database session into FastAPI
    routes or services that need to interact with the database.

    The session is automatically closed after the request lifecycle.

    :param session_provider: The provider responsible for providing PostgreSQL sessions.
    :return: A PostgreSQL database session instance.
    """

    db = session_provider.get_session()
    try:
        yield db
    finally:
        await db.close()
