import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
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
