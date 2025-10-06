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
