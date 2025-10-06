from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path

from src.modules.building.controllers.constants import BuildingCtrlEnums
from src.modules.building.interfaces import IBuildingUC
from src.modules.building.interfaces.controllers import IBuildingCtrl
from src.modules.building.schemas import BuildingWithOrganizations
from src.modules.building.usecases.deps import get_building_usecase


class BuildingCtrl(IBuildingCtrl):
    """Building controller responsible for managing building-related endpoints."""

    def __init__(
        self,
        enums: BuildingCtrlEnums,
    ):
        """
        Initialize the BuildingCtrl with necessary enums and setup routes.

        :param enums: Controller-specific enums including route paths and request types.
        """

        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Return the API router instance.

        :return: Configured APIRouter with building routes.
        """

        return self._controller

    def _add_controllers(self) -> None:
        """Register building-related routes to the controller."""

        self._controller.add_api_route(
            path=self._enums.CtrlPath.organizations_by_building,
            endpoint=self.get_organizations_by_building_sid,
            methods=[self._enums.Common.RequestTypes.GET],
            response_model=BuildingWithOrganizations,
        )

    @staticmethod
    async def get_organizations_by_building_sid(
        building_usecase: Annotated[IBuildingUC, Depends(get_building_usecase)],
        building_sid: UUID = Path(..., alias="buildingSid"),
    ) -> BuildingWithOrganizations:
        """
        Retrieves organizations associated with a specific building by its SID.

        Parameters:

            - building_sid (UUID):
                UUID of the building, passed as a path parameter with alias "buildingSid".

        Returns:
            BuildingWithOrganizations:
                Data structure containing building details and its associated organizations.
        """

        return await building_usecase.get_organizations_by_sid(
            building_sid=building_sid
        )
