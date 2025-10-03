from enum import Enum


class CommonError(Enum):
    """Common system-level errors not specific to a single domain."""

    UNDEFINED = (0, 500, "Unknown error")
    NOT_UNIQUE = (1, 400, "Non-unique field(s) during creation")
    UNPROCESSABLE_ENTITY = (2, 422, "Unprocessable entity")
    ACCESS_DENIED = (3, 403, "Access denied")


class ErrorCodesEnums:
    """Centralized container for all grouped domain-specific error enums."""

    def __init__(self):
        self.Common = CommonError
