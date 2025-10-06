from enum import Enum


class CommonError(Enum):
    """Common system-level errors not specific to a single domain."""

    UNDEFINED = (0, 500, "Unknown error")
    NOT_UNIQUE = (1, 400, "Non-unique field(s) during creation")
    UNPROCESSABLE_ENTITY = (2, 422, "Unprocessable entity")
    ACCESS_DENIED = (3, 403, "Access denied")
    API_KEY_NOT_FOUND = (4, 404, "API key not found")
    INVALID_API_KEY = (5, 500, "Invalid API key")


class ActivityError(Enum):
    EXCEED_MAX_DEPTH = (
        100,
        400,
        "The maximum level of activity nesting has been exceeded (maximum 3 levels).",
    )


class BuildingError(Enum):
    BUILDING_NOT_FOUND = (200, 404, "Building not found")


class ErrorCodesEnums:
    """Centralized container for all grouped domain-specific error enums."""

    def __init__(self):
        self.Common = CommonError
        self.Activity = ActivityError
        self.Building = BuildingError
