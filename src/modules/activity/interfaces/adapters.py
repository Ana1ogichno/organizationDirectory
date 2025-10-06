from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.sql.base import ExecutableOption

from src.common.interfaces import IPostgresBaseRepo
from src.modules.activity.models import ActivityModel
from src.modules.activity.schemas import ActivityCreate, ActivityUpdate


class IActivityPsqlRepo(
    IPostgresBaseRepo[ActivityModel, ActivityCreate, ActivityUpdate], ABC
):
    """
    Interface for a repository managing activity entities in PostgreSQL.

    Defines the contract for classes responsible for CRUD operations and
    business logic related to activity data in the database.
    """

    @abstractmethod
    async def get_by_name(
        self, name: str, custom_options: tuple[ExecutableOption, ...] | None = None
    ) -> ActivityModel:
        """
        Abstract method to retrieve an activity by its name.

        :param name: Name of the activity to search for.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: An instance of ActivityModel matching the given name.
        """
        ...

    @abstractmethod
    async def get_all_descendant_activity_sids(self, activity_name: str) -> list[UUID]:
        """
        Abstract method to retrieve all descendant activity SIDs based on the activity
        name.

        :param activity_name: Name of the root activity.
        :return: List of UUIDs representing all descendant activities including the
                root.
        """
        ...
