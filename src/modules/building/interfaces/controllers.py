from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import APIRouter

from src.modules.building.interfaces import IBuildingUC
from src.modules.building.schemas import BuildingWithOrganizations


class IBuildingCtrl(ABC):
    """
    Interface for building controller defining API router and building retrieval method.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Get the API router instance that exposes building-related endpoints.

        :return: APIRouter instance with user routes
        """

        ...

    @staticmethod
    @abstractmethod
    async def get_organizations_by_building_sid(
        building_sid: UUID,
        building_usecase: IBuildingUC,
    ) -> BuildingWithOrganizations:
        """
        Abstract static method to retrieve organizations associated with a specific
        building SID.

        :param building_sid: UUID of the building.
        :param building_usecase: Instance of IBuildingUC usecase interface.
        :return: BuildingWithOrganizations instance containing related organizations.
        """
        ...
