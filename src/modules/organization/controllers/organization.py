from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.modules.organization.controllers.constants import OrganizationCtrlEnums
from src.modules.organization.interfaces import IOrganizationUC
from src.modules.organization.interfaces.controllers import IOrganizationCtrl
from src.modules.organization.schemas import OrganizationFull
from src.modules.organization.usecases.deps import get_organization_usecase


class OrganizationCtrl(IOrganizationCtrl):
    """
    Organization controller responsible for managing organization-related endpoints.
    """

    def __init__(
        self,
        enums: OrganizationCtrlEnums,
    ):
        """
        Initialize the OrganizationCtrl with necessary enums and setup routes.

        :param enums: Controller-specific enums including route paths and request types.
        """

        self._controller = APIRouter()
        self._enums = enums
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Return the API router instance.

        :return: Configured APIRouter with organization routes.
        """

        return self._controller

    def _add_controllers(self) -> None:
        """Register organization-related routes to the controller."""

        self._controller.add_api_route(
            path=self._enums.CtrlPath.sid,
            endpoint=self.get_by_sid,
            methods=[self._enums.Common.RequestTypes.GET],
            response_model=OrganizationFull,
        )
        self._controller.add_api_route(
            path=self._enums.CtrlPath.activity_descendant,
            endpoint=self.search_by_descendant_activity,
            methods=[self._enums.Common.RequestTypes.GET],
            response_model=list[OrganizationFull],
        )
        self._controller.add_api_route(
            path=self._enums.CtrlPath.activity,
            endpoint=self.search_by_activity,
            methods=[self._enums.Common.RequestTypes.GET],
            response_model=list[OrganizationFull],
        )

    @staticmethod
    async def get_by_sid(
        sid: UUID,
        organization_usecase: Annotated[
            IOrganizationUC, Depends(get_organization_usecase)
        ],
    ) -> OrganizationFull:
        """
        Controller to retrieve full organization details by SID.

        Parameters:

            - sid (UUID):
                UUID of the organization to fetch.

        Returns:
            OrganizationFull:
                Detailed organization data for the given SID.
        """

        return await organization_usecase.get_by_sid(sid=sid)

    @staticmethod
    async def search_by_descendant_activity(
        organization_usecase: Annotated[
            IOrganizationUC, Depends(get_organization_usecase)
        ],
        activity_name: str = Query(..., alias="activityName"),
    ) -> list[OrganizationFull]:
        """
        Controller to search organizations by activity and its descendant activities
        using a provided name.

        Parameters:

            - activityName (str):
                Name of the activity to search by.

        Returns:
            List[OrganizationFull]:
                List of organizations matching the activity represented by the SID.
        """

        return await organization_usecase.search_by_descendant_activity(
            activity_name=activity_name
        )
    
    @staticmethod
    async def search_by_activity(
        organization_usecase: Annotated[
            IOrganizationUC, Depends(get_organization_usecase)
        ],
        activity_name: str = Query(..., alias="activityName"),
    ) -> list[OrganizationFull]:
        """
        Controller to search organizations by activity using a provided name.

        Parameters:

            - activityName (str):
                Name of the activity to search by.

        Returns:
            List[OrganizationFull]:
                List of organizations matching the activity represented by the SID.
        """

        return await organization_usecase.search_by_activity(
            activity_name=activity_name
        )

