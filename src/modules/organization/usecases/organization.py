import logging
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.activity.interfaces import IActivitySrv
from src.modules.organization.interfaces import (
    IOrganizationSrv,
    IOrganizationUC,
)
from src.modules.organization.schemas import OrganizationFull
from src.modules.organization.usecases.constants import OrganizationUCConsts


class OrganizationUC(IOrganizationUC):
    """
    Organization usecase implementation handling organization-related business logic.
    """

    def __init__(
        self,
        consts: OrganizationUCConsts,
        logger: logging.Logger,
        errors: ErrorCodesEnums,
        activity_service: IActivitySrv,
        organization_service: IOrganizationSrv,
    ):
        """
        Initialize the BuildingUC.

        :param consts: OrganizationUCConsts instance containing constant values and options.
        :param logger: Logger instance for logging usecase operations.
        :param errors: ErrorCodesEnums instance for error handling.
        :param activity_service: Service handling activity-related business logic.
        :param organization_service: Service handling organization-related business
                logic.
        """

        self._consts = consts
        self._logger = logger
        self._errors = errors
        self._activity_service = activity_service
        self._organization_service = organization_service

    @LoggingFunctionInfo(
        description="Fetches full organization details by SID using custom options."
    )
    async def get_by_sid(self, sid: UUID) -> OrganizationFull:
        """
        Retrieves a detailed representation of the organization by SID.

        :param sid: UUID of the organization.
        :return: OrganizationFull instance enriched with full data.
        """

        return await self._organization_service.get_by_sid(
            sid=sid,
            custom_options=self._consts.Options.full(),
        )

    @LoggingFunctionInfo(
        description="Search organizations by activity with recursive descendant lookup."
    )
    async def search_by_descendant_activity(self, activity_name: str) -> list[OrganizationFull]:
        """
        Searches organizations linked to the specified activity and its descendant
        activities.

        :param activity_name: The root activity name to search organizations by.
        :return: List of fully detailed OrganizationFull objects.
        """

        activity_sids = await self._activity_service.get_all_descendant_activity_sids(
            activity_name=activity_name,
        )

        return await self._organization_service.get_by_activity_sids(
            activity_sids=activity_sids,
            custom_options=self._consts.Options.full(),
        )

    @LoggingFunctionInfo(
        description="Search organizations by a specific activity name."
    )
    async def search_by_activity(self, activity_name: str) -> list[OrganizationFull]:
        """
        Searches organizations linked to the specified activity name.

        :param activity_name: The activity name to search organizations by.
        :return: List of OrganizationFull instances related to the specified activity.
        """

        activity = await self._activity_service.get_by_name(
            activity_name=activity_name,
        )

        return await self._organization_service.get_by_activity_sids(
            activity_sids=[activity.sid],
            custom_options=self._consts.Options.full(),
        )

