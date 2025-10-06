import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.logger.deps import get_organization_logger
from src.modules.activity.adapters.repositories.postgres.deps import (
    get_activity_psql_repo,
)
from src.modules.activity.interfaces import IActivityPsqlRepo, IActivitySrv
from src.modules.activity.services import ActivitySrv


async def get_activity_service(
    logger: Annotated[logging.Logger, Depends(get_organization_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    activity_psql_repo: Annotated[IActivityPsqlRepo, Depends(get_activity_psql_repo)],
) -> IActivitySrv:
    """
    Factory function to create and return a ActivitySrv instance.

    :param logger: Logger instance for building logs.
    :param error_codes: ErrorCodesEnums instance for error handling.
    :param activity_psql_repo: Repository instance for activity persistence.
    :return: Configured ActivitySrv instance.
    """

    return ActivitySrv(
        errors=error_codes,
        logger=logger,
        activity_psql_repo=activity_psql_repo,
    )
