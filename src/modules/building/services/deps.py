import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.logger.deps import get_building_logger
from src.modules.building.adapters.repositories.postgres.deps import (
    get_building_psql_repo,
)
from src.modules.building.interfaces import IBuildingPsqlRepo, IBuildingSrv
from src.modules.building.services import BuildingSrv


async def get_building_service(
    logger: Annotated[logging.Logger, Depends(get_building_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    building_psql_repo: Annotated[IBuildingPsqlRepo, Depends(get_building_psql_repo)],
) -> IBuildingSrv:
    """
    Factory function to create and return a BuildingSrv instance.

    :param logger: Logger instance for building logs.
    :param error_codes: ErrorCodesEnums instance for error handling.
    :param building_psql_repo: Repository instance for building persistence.
    :return: Configured BuildingSrv instance.
    """

    return BuildingSrv(
        errors=error_codes,
        logger=logger,
        building_psql_repo=building_psql_repo,
    )
