import logging
from uuid import UUID

from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.activity.models import ActivityModel
from src.modules.organization.interfaces import IOrganizationPsqlRepo
from src.modules.organization.models import OrganizationModel
from src.modules.organization.schemas import OrganizationCreate, OrganizationUpdate


class OrganizationPsqlRepo(
    PostgresBaseRepo[OrganizationModel, OrganizationCreate, OrganizationUpdate],
    IOrganizationPsqlRepo,
):
    """Repository implementation for Organization entities using PostgreSQL."""

    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initializes the OrganizationPsqlRepo with database session, error codes, and
        logger.

        :param db: AsyncSession instance for interacting with the database.
        :param errors: Enumeration of error codes for handling repository exceptions.
        :param logger: Logger instance for logging repository operations.
        """

        super().__init__(db=db, model=OrganizationModel, errors=errors, logger=logger)
        self._errors = errors
        self._logger = logger

    @LoggingFunctionInfo(description="Retrieves an organization by its name.")
    async def get_by_name(
        self, name: str, custom_options: tuple[ExecutableOption, ...] | None = None
    ) -> OrganizationModel | None:
        """
        Fetches a single organization with the specified name.

        :param name: The name of the organization.
        :param custom_options: Optional tuple of SQL execution options, such as query
                hints.
        :return: OrganizationModel instance matching the given name.
        """

        query = await self._apply_options(
            query=select(self._model).where(self._model.name == name),
            options=custom_options,
        )

        self._logger.debug("Retrieved organization by name: %s", name)
        return await self._get_single_result(query)

    @LoggingFunctionInfo(
        description="Retrieve organizations linked to specified activity SIDs using "
        "customized query options."
    )
    async def get_by_activity_sids(
        self,
        activity_sids: list[UUID],
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> Sequence[OrganizationModel | None]:
        """
        Retrieves organizations linked to any of the specified activity SIDs.

        :param activity_sids: List of activity UUIDs to filter organizations by their
                associated activities.
        :param custom_options: Optional tuple of SQLAlchemy execution options to
                customize the query.
        :return: Sequence of OrganizationModel instances or None.
        """

        query = select(self._model).join(self._model.activities).distinct()

        query = await self._apply_options(
            query=query.where(ActivityModel.sid.in_(activity_sids)),
            options=custom_options,
        )

        return await self._get_all_results(query)

    @LoggingFunctionInfo(
        description="Search activities by name using case-insensitive partial match."
    )
    async def search_by_name(
        self,
        name: str,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> Sequence[OrganizationModel | None]:
        """
        Performs a case-insensitive search for activities matching the given name pattern.

        :param name: Name pattern to look for.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: Sequence of matching OrganizationModel instances or None.
        """

        query = select(self._model).where(self._model.name.ilike(f"%{name}%"))

        query = await self._apply_options(query=query, options=custom_options)

        return await self._get_all_results(query)
