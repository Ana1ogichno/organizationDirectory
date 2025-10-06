import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.logger.deps import get_organization_logger
from src.modules.organization.interfaces import IOrganizationSrv, IOrganizationUC
from src.modules.organization.services.deps import get_organization_service
from src.modules.organization.usecases import OrganizationUC
from src.modules.organization.usecases.constants import OrganizationUCConsts
from src.modules.organization.usecases.constants.deps import get_organization_uc_consts


async def get_organization_usecase(
    consts: Annotated[OrganizationUCConsts, Depends(get_organization_uc_consts)],
    logger: Annotated[logging.Logger, Depends(get_organization_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    organization_service: Annotated[
        IOrganizationSrv, Depends(get_organization_service)
    ],
) -> IOrganizationUC:
    """
    Factory function to create and return a OrganizationUC instance.

    :param consts: OrganizationUCConsts instance with use case constants.
    :param logger: Logger instance for organization use case logs.
    :param error_codes: ErrorCodesEnums instance for error handling.
    :param organization_service: Service instance for organization business logic.
    :return: Configured OrganizationUC instance.
    """

    return OrganizationUC(
        consts=consts,
        logger=logger,
        errors=error_codes,
        organization_service=organization_service,
    )
