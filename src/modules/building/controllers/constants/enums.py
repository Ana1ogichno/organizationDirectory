from enum import StrEnum

from src.common.constants import CommonEnums


class CtrlPath(StrEnum):
    """Enum defining route paths for building controller endpoints."""

    organizations_by_building = "/{buildingSid}/organizations"
    by_coordinates = "/coordinates"


class BuildingCtrlEnums:
    """Container for enums used in the building controller layer."""

    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        """
        Initialize UserCtrlEnums with shared application enums.

        :param common_enums: CommonEnums instance used across multiple modules.
        """

        self.CtrlPath = CtrlPath
        self.Common = common_enums
