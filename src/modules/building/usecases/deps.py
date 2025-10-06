import logging
from typing import Annotated

from fastapi import Depends

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.logger.deps import get_building_logger
from src.modules.building.interfaces import IBuildingSrv, IBuildingUC
from src.modules.building.services.deps import get_building_service
from src.modules.building.usecases import BuildingUC
from src.modules.building.usecases.constants import BuildingUCConsts
from src.modules.building.usecases.constants.deps import get_building_uc_consts


async def get_building_usecase(
    consts: Annotated[BuildingUCConsts, Depends(get_building_uc_consts)],
    logger: Annotated[logging.Logger, Depends(get_building_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    building_service: Annotated[IBuildingSrv, Depends(get_building_service)],
) -> IBuildingUC:
    """
    Factory function to create and return a BuildingUC instance.

    :param consts: BuildingUCConsts instance with use case constants.
    :param logger: Logger instance for building use case logs.
    :param error_codes: ErrorCodesEnums instance for error handling.
    :param building_service: Service instance for building business logic.
    :return: Configured BuildingUC instance.
    """

    return BuildingUC(
        consts=consts,
        logger=logger,
        errors=error_codes,
        building_service=building_service,
    )
