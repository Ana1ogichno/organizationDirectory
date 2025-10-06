import logging
from uuid import UUID

from src.common.constants import ErrorCodesEnums
from src.common.decorators.logger import LoggingFunctionInfo
from src.modules.activity.interfaces import IActivityPsqlRepo, IActivitySrv
from src.modules.activity.schemas import Activity


class ActivitySrv(IActivitySrv):
    """Service for activity-related operations."""

    def __init__(
        self,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        activity_psql_repo: IActivityPsqlRepo,
    ):
        """
        Initialize the BuildingSrv.

        :param errors: ErrorCodesEnums instance for error handling.
        :param logger: Logger instance for logging service actions.
        :param activity_psql_repo: Repository for activity persistence
                operations.
        """

        self._errors = errors
        self._logger = logger
        self._activity_psql_repo = activity_psql_repo

    @LoggingFunctionInfo(
        description="Delegate retrieval of descendant activity SIDs to the activity "
        "postgres repository."
    )
    async def get_all_descendant_activity_sids(self, activity_name: str) -> list[UUID]:
        """
        Fetches all descendant activity SIDs by delegating to the associated repository.

        :param activity_name: The root activity name to fetch descendants for.
        :return: List of descendant activity UUIDs.
        """

        return await self._activity_psql_repo.get_all_descendant_activity_sids(
            activity_name=activity_name
        )

    @LoggingFunctionInfo(
        description="Retrieve activity by its name with model validation."
    )
    async def get_by_name(self, activity_name: str) -> Activity:
        """
        Retrieves an activity instance by name from the data repository and validates it.

        :param activity_name: The name of the activity to retrieve.
        :return: Validated Activity instance.
        """

        return Activity.model_validate(
            await self._activity_psql_repo.get_by_name(name=activity_name)
        )
