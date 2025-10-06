import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.deps import get_db
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.logger.deps import get_organization_logger
from src.modules.organization.adapters.repositories.postgres import (
    OrganizationActivityPsqlRepo,
    OrganizationAddressPsqlRepo,
    OrganizationPsqlRepo,
    PhoneNumberPsqlRepo,
)
from src.modules.organization.interfaces import (
    IOrganizationActivityPsqlRepo,
    IOrganizationAddressPsqlRepo,
    IOrganizationPsqlRepo,
    IPhoneNumberPsqlRepo,
)


async def get_phone_number_psql_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_organization_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
) -> IPhoneNumberPsqlRepo:
    """
    Provides an instance of PhoneNumberPsqlRepo using injected dependencies.

    :param db: AsyncSession dependency for database operations.
    :param logger: Logger dependency configured for building logs.
    :param error_codes: ErrorCodesEnums dependency for error handling.
    :return: Instance of IPhoneNumberPsqlRepo.
    """

    return PhoneNumberPsqlRepo(db=db, errors=error_codes, logger=logger)


async def get_organization_psql_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_organization_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
) -> IOrganizationPsqlRepo:
    """
    Provides an instance of OrganizationPsqlRepo using injected dependencies.

    :param db: AsyncSession dependency for database operations.
    :param logger: Logger dependency configured for building logs.
    :param error_codes: ErrorCodesEnums dependency for error handling.
    :return: Instance of IOrganizationPsqlRepo.
    """

    return OrganizationPsqlRepo(db=db, errors=error_codes, logger=logger)


async def get_organization_address_psql_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_organization_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
) -> IOrganizationAddressPsqlRepo:
    """
    Provides an instance of OrganizationAddressPsqlRepo using injected dependencies.

    :param db: AsyncSession dependency for database operations.
    :param logger: Logger dependency configured for building logs.
    :param error_codes: ErrorCodesEnums dependency for error handling.
    :return: Instance of IOrganizationAddressPsqlRepo.
    """

    return OrganizationAddressPsqlRepo(db=db, errors=error_codes, logger=logger)


async def get_organization_activity_psql_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_organization_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
) -> IOrganizationActivityPsqlRepo:
    """
    Provides an instance of OrganizationActivityPsqlRepo using injected dependencies.

    :param db: AsyncSession dependency for database operations.
    :param logger: Logger dependency configured for building logs.
    :param error_codes: ErrorCodesEnums dependency for error handling.
    :return: Instance of IOrganizationActivityPsqlRepo.
    """

    return OrganizationActivityPsqlRepo(db=db, errors=error_codes, logger=logger)
