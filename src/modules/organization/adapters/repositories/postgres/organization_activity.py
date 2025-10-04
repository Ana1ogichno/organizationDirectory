import logging
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.organization.interfaces import (
    IOrganizationActivityPsqlRepo,
)
from src.modules.organization.models.organization import OrganizationActivityModel
from src.modules.organization.schemas import (
    OrganizationActivityCreate,
    OrganizationActivityUpdate,
)


class OrganizationActivityPsqlRepo(
    PostgresBaseRepo[
        OrganizationActivityModel,
        OrganizationActivityCreate,
        OrganizationActivityUpdate,
    ],
    IOrganizationActivityPsqlRepo,
):
    """Repository for handling OrganizationActivity entities in PostgreSQL."""

    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initialize the OrganizationActivityPsqlRepo.

        :param db: AsyncSession instance.
        :param errors: ErrorCodesEnums instance.
        :param logger: Logger instance.
        """

        super().__init__(
            db=db, model=OrganizationActivityModel, errors=errors, logger=logger
        )
        self._errors = errors
        self._logger = logger

    @LoggingFunctionInfo(
        description="Retrieves an organization activity by organization and activity "
        "IDs."
    )
    async def get_by_organization_and_activity_sids(
        self,
        activity_sid: UUID,
        organization_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> OrganizationActivityModel | None:
        """
        Fetches an organization activity corresponding to specified organization and activity.

        :param activity_sid: UUID of the activity.
        :param organization_sid: UUID of the organization.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: OrganizationActivityModel if found, else None.
        """
        query = await self._apply_options(
            query=select(self._model).where(
                and_(
                    self._model.organization_sid == organization_sid,
                    self._model.activity_sid == activity_sid,
                )
            ),
            options=custom_options,
        )

        self._logger.debug(
            "Retrieved organization activity by organization sid %s and activity sid: %s",
            organization_sid,
            activity_sid,
        )
        return await self._get_single_result(query)
