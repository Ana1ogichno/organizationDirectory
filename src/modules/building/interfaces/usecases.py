from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.building.schemas import BuildingWithOrganizations


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
