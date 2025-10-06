from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.organization.schemas import OrganizationFull


class IOrganizationUC(ABC):
    """
    Interface for organization use case containing organization-related business logic.
    """

    @abstractmethod
    async def get_by_sid(self, sid: UUID) -> OrganizationFull:
        """
        Abstract method to fetch full organization details by SID.

        :param sid: UUID of the organization.
        :return: OrganizationFull instance with detailed organization data.
        """
        ...

    @abstractmethod
    async def search_by_activity(self, activity_name: str) -> list[OrganizationFull]:
        """
        Abstract method to search organizations by activity name.

        :param activity_name: Name of the activity to search by.
        :return: List of OrganizationFull instances matching the activity.
        """
        ...
