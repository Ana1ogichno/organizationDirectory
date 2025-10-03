from src.common.constants import CommonEnums, ErrorCodesEnums


def get_error_codes() -> ErrorCodesEnums:
    """
    Dependency provider for error code enums.

    This function returns an instance of `ErrorCodesEnums`, which implements
    the `IErrorCodesEnums` interface and provides standardized application error codes
    used for exception handling throughout the application.

    :return: An instance of `ErrorCodesEnums` implementing `IErrorCodesEnums`.
    """

    return ErrorCodesEnums()


def get_common_enums() -> CommonEnums:
    """
    Dependency provider for HTTP request type enumerations.

    This function returns the `RequestTypes` class, which is a `StrEnum` enumeration
    containing all standard HTTP request methods (GET, POST, PUT, etc.).
    The enum values are string representations of the HTTP methods.

    :return: The `RequestTypes` enum class containing HTTP method constants.
    """

    return CommonEnums()
