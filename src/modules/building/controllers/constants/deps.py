from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.building.controllers.constants import BuildingCtrlEnums


def get_building_ctrl_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) -> BuildingCtrlEnums:
    """
    Dependency provider for BuildingCtrlEnums.

    :return: Instance of BuildingCtrlEnums.
    """

    return BuildingCtrlEnums(common_enums=common_enums)
