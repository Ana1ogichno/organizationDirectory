from abc import ABC, abstractmethod


class IPostgresInitializer(ABC):
    """
    Interface for PostgresInitializer that defines methods required to initialize
    the database and create initial system data.
    """

    @abstractmethod
    async def init(self) -> None:
        """
        Performs all necessary initialization steps, such as creating the default
        superuser account and committing changes to the database.
        """
        ...
