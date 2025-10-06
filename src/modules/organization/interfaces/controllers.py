from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter

from src.modules.organization.interfaces import IOrganizationUC
from src.modules.organization.schemas import OrganizationFull


class IOrganizationCtrl(ABC):
    """
    Interface for organization controller defining API router and organization
    retrieval method.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the API router instance that exposes organization-related endpoints.

        :return: APIRouter instance with organization routes
        """

        ...

    @staticmethod
    @abstractmethod
    async def get_by_sid(
        sid: UUID,
        organization_usecase: IOrganizationUC,
    ) -> OrganizationFull:
        """
        Abstract static method to retrieve full organization details by SID using the
        given use case.

        :param sid: UUID of the organization.
        :param organization_usecase: Instance of IOrganizationUC use case for
                organization logic.
        :return: OrganizationFull instance containing detailed organization data.
        """
        ...

    @staticmethod
    @abstractmethod
    async def search_by_activity(
        organization_usecase: IOrganizationUC,
        activity_name: str,
    ) -> list[OrganizationFull]:
        """
        Abstract static method to search organizations by activity name using the
        provided organization use case.

        :param organization_usecase: Instance of IOrganizationUC use case interface.
        :param activity_name: Activity name string to search organizations by.
        :return: List of OrganizationFull instances representing matching organizations.
        """
        ...
