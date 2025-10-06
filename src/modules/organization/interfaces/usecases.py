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
    async def search_by_descendant_activity(
        self, activity_name: str
    ) -> list[OrganizationFull]:
        """
        Abstract method to search organizations by descendant activity name.

        :param activity_name: Name of the activity to search organizations by,
                including descendants.
        :return: List of OrganizationFull instances matching the activity and its
                descendants.
        """
        ...

    @abstractmethod
    async def search_by_activity(self, activity_name: str) -> list[OrganizationFull]:
        """
        Abstract method to search organizations by activity name.

        :param activity_name: Name of the activity to search organizations by.
        :return: List of OrganizationFull instances matching the activity.
        """
        ...

    @abstractmethod
    async def search_by_name(self, name: str) -> list[OrganizationFull]:
        """
        Abstract method to search organizations by name with full option.

        :param name: Name or partial name of organizations to search for.
        :return: List of OrganizationFull instances matching the name.
        """
        ...
