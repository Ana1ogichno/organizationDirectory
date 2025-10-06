import logging
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.building.interfaces import IBuildingSrv, IBuildingUC
from src.modules.building.schemas import BuildingWithOrganizations
from src.modules.building.usecases.constants import BuildingUCConsts


class BuildingUC(IBuildingUC):
    """Building usecase implementation handling building-related business logic."""

    def __init__(
        self,
        consts: BuildingUCConsts,
        logger: logging.Logger,
        errors: ErrorCodesEnums,
        building_service: IBuildingSrv,
    ):
        """
        Initialize the BuildingUC.

        :param consts: BuildingUCConsts instance containing constant values and options.
        :param logger: Logger instance for logging usecase operations.
        :param errors: ErrorCodesEnums instance for error handling.
        :param building_service: Service handling building-related business logic.
        """

        self._consts = consts
        self._logger = logger
        self._errors = errors
        self._building_service = building_service

    @LoggingFunctionInfo(
        description="Retrieves organizations for a building by its SID."
    )
    async def get_organizations_by_sid(
        self, building_sid: UUID
    ) -> BuildingWithOrganizations:
        """
        Fetches organizations associated with a given building SID.

        :param building_sid: UUID of the building to retrieve organizations for.
        :return: BuildingWithOrganizations instance containing building and its
                organizations.
        """

        return await self._building_service.get_by_sid(
            building_sid=building_sid,
            custom_options=self._consts.Options.with_organizations(),
        )
