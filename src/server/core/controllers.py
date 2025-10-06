from fastapi import APIRouter

from src.common.constants.deps import get_common_enums
from src.modules.building.controllers.constants.deps import get_building_ctrl_enums
from src.modules.building.controllers.deps import get_building_controllers
from src.modules.organization.controllers.constants.deps import \
    get_organization_ctrl_enums
from src.modules.organization.controllers.deps import get_organization_controllers

api_controller = APIRouter()

api_controller.include_router(
    get_building_controllers(
        get_building_ctrl_enums(
            get_common_enums(),
        ),
    ).controller,
    tags=["Building"],
    prefix="/buildings",
)

api_controller.include_router(
    get_organization_controllers(
        get_organization_ctrl_enums(
            get_common_enums(),
        ),
    ).controller,
    tags=["Organization"],
    prefix="/organizations",
)

