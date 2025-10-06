from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.building.filters import BuildingCoordinatesFilter
from src.modules.organization.schemas import BuildingWithOrganizations


class IBuildingUC(ABC):
    """Interface for building use case containing building-related business logic."""

    @abstractmethod
    async def get_organizations_by_sid(
        self, building_sid: UUID
    ) -> BuildingWithOrganizations:
        """
        Abstract method to retrieve organizations associated with a given building SID.

        :param building_sid: UUID of the building.
        :return: BuildingWithOrganizations instance containing related organizations.
        """
        ...

    @abstractmethod
    async def get_filtered_list(
        self,
        filters: BuildingCoordinatesFilter,
    ) -> list[BuildingWithOrganizations | None]:
        """
        Abstract method to retrieve a filtered list of buildings with organizations.

        :param filters: BuildingCoordinatesFilter instance defining filtering criteria.
        :return: List of BuildingWithOrganizations instances.
        """
        ...
