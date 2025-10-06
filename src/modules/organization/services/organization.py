import logging
from uuid import UUID

from sqlalchemy.sql.base import ExecutableOption

from src.common.constants import ErrorCodesEnums
from src.common.decorators.logger import LoggingFunctionInfo
from src.modules.organization.interfaces import IOrganizationPsqlRepo, IOrganizationSrv
from src.modules.organization.schemas import OrganizationFull
from src.server.middleware.exception import BackendException


class OrganizationSrv(IOrganizationSrv):
    """Service for organization-related operations."""

    def __init__(
        self,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        organization_psql_repo: IOrganizationPsqlRepo,
    ):
        """
        Initialize the BuildingSrv.

        :param errors: ErrorCodesEnums instance for error handling.
        :param logger: Logger instance for logging service actions.
        :param organization_psql_repo: Repository for organization persistence
                operations.
        """

        self._errors = errors
        self._logger = logger
        self._organization_psql_repo = organization_psql_repo

    @LoggingFunctionInfo(
        description="Retrieves an organization by SID with optional query options."
    )
    async def get_by_sid(
        self, sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> OrganizationFull:
        """
        Fetches an organization model by SID, validates presence, and logs the process.

        :param sid: UUID of the organization to retrieve.
        :param custom_options: Optional SQLAlchemy query customization options.
        :raises BackendException: If organization is not found.
        :return: Validated OrganizationFull instance of the retrieved organization.
        """

        organization = await self._organization_psql_repo.get(
            sid=sid, custom_options=custom_options
        )

        if not organization:
            self._logger.error("Organization not found with SID: %s", sid)
            raise BackendException(self._errors.Building.BUILDING_NOT_FOUND)

        self._logger.debug("Organization successfully retrieved with SID: %s", sid)

        return OrganizationFull.model_validate(organization)

    @LoggingFunctionInfo(
        description="Retrieve full organizations by activity SIDs and validate models."
    )
    async def get_by_activity_sids(
        self,
        activity_sids: list[UUID],
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> list[OrganizationFull]:
        """
        Fetch organizations linked to the given activity SIDs and validate as OrganizationFull models.

        :param activity_sids: List of activity UUIDs for filtering.
        :param custom_options: Optional query execution options.
        :return: List of OrganizationFull validated instances.
        """

        organizations = await self._organization_psql_repo.get_by_activity_sids(
            activity_sids=activity_sids, custom_options=custom_options
        )

        return [
            OrganizationFull.model_validate(organization)
            for organization in organizations
        ]

    @LoggingFunctionInfo(
        description="Search organizations by name and validate results with "
        "OrganizationFull models."
    )
    async def search_by_name(
        self,
        name: str,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> list[OrganizationFull]:
        """
        Performs a search for organizations by name in the repository and validates the
        results.

        :param name: Name filter for searching organizations.
        :param custom_options: Optional execution options for the query.
        :return: List of validated OrganizationFull instances.
        """

        organizations = await self._organization_psql_repo.search_by_name(
            name=name, custom_options=custom_options
        )

        return [
            OrganizationFull.model_validate(organization)
            for organization in organizations
        ]
