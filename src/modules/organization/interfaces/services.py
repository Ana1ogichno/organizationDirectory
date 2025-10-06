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
