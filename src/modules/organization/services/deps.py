import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.logger.deps import get_organization_logger
from src.modules.organization.adapters.repositories.postgres.deps import (
    get_organization_psql_repo,
)
from src.modules.organization.interfaces import (
    IOrganizationPsqlRepo,
    IOrganizationSrv,
)
from src.modules.organization.services import OrganizationSrv


async def get_organization_service(
    logger: Annotated[logging.Logger, Depends(get_organization_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    organization_psql_repo: Annotated[
        IOrganizationPsqlRepo, Depends(get_organization_psql_repo)
    ],
) -> IOrganizationSrv:
    """
    Factory function to create and return a OrganizationSrv instance.

    :param logger: Logger instance for building logs.
    :param error_codes: ErrorCodesEnums instance for error handling.
    :param organization_psql_repo: Repository instance for building persistence.
    :return: Configured OrganizationSrv instance.
    """

    return OrganizationSrv(
        errors=error_codes,
        logger=logger,
        organization_psql_repo=organization_psql_repo,
    )
