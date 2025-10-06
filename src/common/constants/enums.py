from enum import StrEnum


class RequestTypesEnum(StrEnum):
    """
    Enumeration of standard HTTP request methods.

    Provides string constants for all HTTP methods (GET, POST, PUT, etc.)
    as case-sensitive uppercase values. Inherits from `StrEnum`, allowing
    direct string comparison.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    TRACE = "TRACE"
    CONNECT = "CONNECT"


class CommonEnums:
    """
    Container for commonly used enumerations.

    Provides access to shared enum types such as HTTP request methods.
    Centralizes enum definitions to ensure consistency and ease of reuse
    across the application.
    """

    def __init__(self):
        """Initializes the CommonEnums container."""

        self.RequestTypes = RequestTypesEnum
