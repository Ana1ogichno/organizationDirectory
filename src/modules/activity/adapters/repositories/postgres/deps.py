import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.deps import get_db
from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.logger.deps import get_activity_logger
from src.modules.activity.adapters.repositories.postgres import ActivityPsqlRepo
from src.modules.activity.interfaces import IActivityPsqlRepo


async def get_activity_psql_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_activity_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
) -> IActivityPsqlRepo:
    """
    Provides an instance of ActivityPsqlRepo using injected dependencies.

    :param db: AsyncSession dependency for database operations.
    :param logger: Logger dependency configured for building logs.
    :param error_codes: ErrorCodesEnums dependency for error handling.
    :return: Instance of IActivityPsqlRepo.
    """

    return ActivityPsqlRepo(db=db, errors=error_codes, logger=logger)
