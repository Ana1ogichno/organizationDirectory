from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.activity.schemas import Activity


class IActivitySrv(ABC):
    """
    Interface for activity service defining core activity operations.
    """

    @abstractmethod
    async def get_all_descendant_activity_sids(self, activity_name: str) -> list[UUID]:
        """
        Abstract method to retrieve all descendant activity SIDs by activity name.

        :param activity_name: Name of the activity root.
        :return: List of UUIDs representing all descendant activities.
        """
        ...

    @abstractmethod
    async def get_by_name(self, activity_name: str) -> Activity:
        """
        Abstract method to retrieve an activity by its name.

        :param activity_name: Name of the activity to retrieve.
        :return: Activity instance representing the found activity.
        """
        ...
