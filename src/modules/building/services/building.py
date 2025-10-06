import logging
from uuid import UUID

from sqlalchemy.sql.base import ExecutableOption

from src.common.constants import ErrorCodesEnums
from src.common.decorators.logger import LoggingFunctionInfo
from src.modules.building.filters import BuildingCoordinatesFilter
from src.modules.building.interfaces import IBuildingPsqlRepo, IBuildingSrv
from src.modules.building.schemas import BuildingWithOrganizations
from src.server.middleware.exception import BackendException


class BuildingSrv(IBuildingSrv):
    """Service for building-related operations."""

    def __init__(
        self,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        building_psql_repo: IBuildingPsqlRepo,
    ):
        """
        Initialize the BuildingSrv.

        :param errors: ErrorCodesEnums instance for error handling.
        :param logger: Logger instance for logging service actions.
        :param building_psql_repo: Repository for building persistence operations.
        """

        self._errors = errors
        self._logger = logger
        self._building_psql_repo = building_psql_repo

    @LoggingFunctionInfo(
        description="Retrieves building by SID and returns it with associated "
        "organizations."
    )
    async def get_by_sid(
        self, building_sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> BuildingWithOrganizations:
        """
        Fetches a building by its SID and returns a validated BuildingWithOrganizations
        model.

        :param building_sid: UUID of the building to retrieve.
        :param custom_options: Optional SQLAlchemy execution options to apply to the
                repository call.
        :return: BuildingWithOrganizations instance validated from the retrieved
                building model.
        """

        building = await self._building_psql_repo.get(
            sid=building_sid, custom_options=custom_options
        )

        if not building:
            self._logger.error("Building not found with SID: %s", building_sid)
            raise BackendException(self._errors.Building.BUILDING_NOT_FOUND)

        self._logger.debug("Building successfully retrieved with SID: %s", building_sid)
        return BuildingWithOrganizations.model_validate(building)

    @LoggingFunctionInfo(
        description="Retrieves buildings filtered by coordinates and returns them with "
        "associated organizations."
    )
    async def get_filtered_all(
        self,
        filters: BuildingCoordinatesFilter,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> list[BuildingWithOrganizations | None]:
        """
        Retrieves buildings filtered by coordinates and converts them to
        BuildingWithOrganizations models. Logs the number of buildings found.

        :param filters: BuildingCoordinatesFilter instance specifying filter criteria.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: List of BuildingWithOrganizations instances or None.
        """

        buildings = await self._building_psql_repo.get_filtered_all(
            filters=filters, custom_options=custom_options
        )

        self._logger.debug(
            "Filtered and retrieved %d buildings with organizations", len(buildings)
        )

        return [
            BuildingWithOrganizations.model_validate(building) for building in buildings
        ]
