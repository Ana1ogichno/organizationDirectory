from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


class IPostgresSessionProvider(ABC):
    """
    Abstract interface for providing PostgreSQL async sessions.

    Implementations of this interface must return an active AsyncSession instance,
    typically used within a request lifecycle or a transactional scope.

    This abstraction helps decouple database access logic from concrete session
    creation, supporting better testability and adherence to the Dependency Inversion
    Principle.
    """

    @abstractmethod
    def get_session(self) -> async_scoped_session[AsyncSession]:
        """
        Retrieve an active PostgreSQL async session.

        :return: Instance of AsyncSession for executing database operations.
        """
        ...
