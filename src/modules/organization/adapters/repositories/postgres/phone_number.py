import logging
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.organization.interfaces import IPhoneNumberPsqlRepo
from src.modules.organization.models.organization import PhoneNumberModel
from src.modules.organization.schemas import (
    PhoneNumberCreate,
    PhoneNumberUpdate,
)


class PhoneNumberPsqlRepo(
    PostgresBaseRepo[PhoneNumberModel, PhoneNumberCreate, PhoneNumberUpdate],
    IPhoneNumberPsqlRepo,
):
    """Repository implementation for PhoneNumber entities using PostgreSQL."""

    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initializes the PhoneNumberPsqlRepo with database session, error codes, and logger.

        :param db: AsyncSession instance for database connectivity.
        :param errors: Enumeration of error codes for repository exceptions.
        :param logger: Logger instance for logging repository operations.
        """

        super().__init__(db=db, model=PhoneNumberModel, errors=errors, logger=logger)
        self._errors = errors
        self._logger = logger

    @LoggingFunctionInfo(
        description="Retrieves a phone number by organization SID and phone string."
    )
    async def get_by_organization_and_phone(
        self,
        organization_sid: UUID,
        phone: str,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> PhoneNumberModel | None:
        """
        Fetches a phone number record matching the given organization SID and phone.

        :param organization_sid: UUID of the organization owning the phone number.
        :param phone: Phone number string to match.
        :param custom_options: Optional tuple of SQLAlchemy execution options like
                query hints.
        :return: PhoneNumberModel instance matching the criteria or None if not found.
        """

        query = await self._apply_options(
            query=select(self._model).where(
                and_(
                    self._model.organization_sid == organization_sid,
                    self._model.phone == phone,
                )
            ),
            options=custom_options,
        )

        self._logger.debug(
            "Retrieved organization phone by organization sid %s and phone: %s",
            organization_sid,
            phone,
        )
        return await self._get_single_result(query)
