from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.sql.base import ExecutableOption

from src.modules.organization.schemas import OrganizationFull


class IOrganizationSrv(ABC):
    """
    Interface for organization service defining core organization operations.
    """

    @abstractmethod
    async def get_by_sid(
        self, sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> OrganizationFull:
        """
        Abstract method to retrieve an organization by its SID.

        :param sid: UUID of the organization.
        :param custom_options: Optional tuple of SQLAlchemy ExecutableOptions for query
                customization.
        :return: OrganizationFull instance representing full organization details.
        """
        ...

    @abstractmethod
    async def get_by_activity_sids(
        self,
        activity_sids: list[UUID],
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> list[OrganizationFull]:
        """
        Abstract method to retrieve full organization details by activity SIDs.

        :param activity_sids: List of UUIDs for activity filtering.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: List of OrganizationFull instances.
        """
        ...
