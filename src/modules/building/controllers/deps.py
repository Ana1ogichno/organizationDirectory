from typing import Annotated

from fastapi import Depends

from src.modules.building.controllers import BuildingCtrl
from src.modules.building.controllers.constants import BuildingCtrlEnums
from src.modules.building.controllers.constants.deps import get_building_ctrl_enums
from src.modules.building.interfaces.controllers import IBuildingCtrl


def get_building_controllers(
    enums: Annotated[BuildingCtrlEnums, Depends(get_building_ctrl_enums)],
) -> IBuildingCtrl:
    """
    Dependency provider for the building controller.

    :param enums: Enum container used within building controller logic.
    :return: Instance of IBuildingCtrl.
    """

    return BuildingCtrl(enums=enums)
