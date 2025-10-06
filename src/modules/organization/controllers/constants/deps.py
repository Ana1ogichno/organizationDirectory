from typing import Annotated

from fastapi import Depends

from src.common.constants import CommonEnums
from src.common.constants.deps import get_common_enums
from src.modules.organization.controllers.constants import OrganizationCtrlEnums


def get_organization_ctrl_enums(
    common_enums: Annotated[CommonEnums, Depends(get_common_enums)],
) -> OrganizationCtrlEnums:
    """
    Dependency provider for OrganizationCtrlEnums.

    :return: Instance of OrganizationCtrlEnums.
    """

    return OrganizationCtrlEnums(common_enums=common_enums)
