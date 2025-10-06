from typing import Annotated

from fastapi import Depends

from src.modules.organization.controllers.constants import OrganizationCtrlEnums
from src.modules.organization.controllers.constants.deps import (
    get_organization_ctrl_enums,
)
from src.modules.organization.controllers import OrganizationCtrl
from src.modules.organization.interfaces.controllers import IOrganizationCtrl


def get_organization_controllers(
    enums: Annotated[OrganizationCtrlEnums, Depends(get_organization_ctrl_enums)],
) -> IOrganizationCtrl:
    """
    Dependency provider for the organization controller.

    :param enums: Enum container used within organization controller logic.
    :return: Instance of IOrganizationCtrl.
    """

    return OrganizationCtrl(enums=enums)
