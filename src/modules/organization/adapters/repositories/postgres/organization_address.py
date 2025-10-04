import logging
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.organization.interfaces import IOrganizationAddressPsqlRepo
from src.modules.organization.models import OrganizationAddressModel
from src.modules.organization.schemas import (
    OrganizationAddressCreate,
    OrganizationAddressUpdate,
)


class OrganizationAddressPsqlRepo(
    PostgresBaseRepo[
        OrganizationAddressModel, OrganizationAddressCreate, OrganizationAddressUpdate
    ],
    IOrganizationAddressPsqlRepo,
):
    """Repository for handling OrganizationAddress entities in PostgreSQL."""

    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initialize the OrganizationAddressPsqlRepo.

        :param db: AsyncSession instance.
        :param errors: ErrorCodesEnums instance.
        :param logger: Logger instance.
        """

        super().__init__(
            db=db, model=OrganizationAddressModel, errors=errors, logger=logger
        )
        self._errors = errors
        self._logger = logger

    @LoggingFunctionInfo(
        description="Retrieves an organization address by organization and building "
        "IDs."
    )
    async def get_by_organization_and_building_sids(
        self,
        building_sid: UUID,
        organization_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> OrganizationAddressModel | None:
        """
        Fetches an organization address corresponding to specified organization and
        building.

        :param building_sid: UUID of the building.
        :param organization_sid: UUID of the organization.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: OrganizationAddressModel if found, else None.
        """

        query = await self._apply_options(
            query=select(self._model).where(
                and_(
                    self._model.organization_sid == organization_sid,
                    self._model.building_sid == building_sid,
                )
            ),
            options=custom_options,
        )

        self._logger.debug(
            "Retrieved organization address by organization sid %s and building sid: %s",
            organization_sid,
            building_sid,
        )
        return await self._get_single_result(query)
