from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.sql.base import ExecutableOption

from src.modules.building.filters import BuildingCoordinatesFilter
from src.modules.organization.schemas import BuildingWithOrganizations


class IBuildingSrv(ABC):
    """
    Interface for building service defining core building operations.
    """

    @abstractmethod
    async def get_by_sid(
        self, building_sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> BuildingWithOrganizations:
        """
        Abstract method to fetch a building by its SID with optional custom query
        options.

        :param building_sid: UUID of the building to retrieve.
        :param custom_options: Optional tuple of SQLAlchemy ExecutableOptions for
                query customization.
        :return: BuildingWithOrganizations instance including associated organizations.
        """
        ...

    @abstractmethod
    async def get_filtered_all(
        self,
        filters: BuildingCoordinatesFilter,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> list[BuildingWithOrganizations | None]:
        """
        Abstract method to retrieve buildings filtered by specified coordinates,
        returning a list of BuildingWithOrganizations models.

        :param filters: BuildingCoordinatesFilter instance with filtering criteria.
        :param custom_options: Optional tuple of SQLAlchemy ExecutableOptions for query
                customization.
        :return: List of BuildingWithOrganizations instances or None.
        """
        ...
