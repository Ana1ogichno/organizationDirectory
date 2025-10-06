from enum import StrEnum

from src.common.constants import CommonEnums


class CtrlPath(StrEnum):
    """Enum defining route paths for organization controller endpoints."""

    sid = "/{sid}"
    activity_descendant = "/search/activity/descendant"
    activity = "/search/activity"
    by_name = "/search/name"


class OrganizationCtrlEnums:
    """Container for enums used in the organization controller layer."""

    def __init__(
        self,
        common_enums: CommonEnums,
    ):
        """
        Initialize OrganizationCtrlEnums with shared application enums.

        :param common_enums: CommonEnums instance used across multiple modules.
        """

        self.CtrlPath = CtrlPath
        self.Common = common_enums
