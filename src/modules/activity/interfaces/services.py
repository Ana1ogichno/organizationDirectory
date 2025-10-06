from abc import ABC, abstractmethod
from uuid import UUID


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
