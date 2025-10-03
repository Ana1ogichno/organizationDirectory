from src.common.logger.constants import LoggerConfigEnums


def get_logger_config() -> LoggerConfigEnums:
    """
    Dependency provider for error code enums.

    This function returns an instance of `ErrorCodesEnums`, which implements
    the `IErrorCodesEnums` interface and provides standardized application error codes
    used for exception handling throughout the application.

    :return: An instance of `ErrorCodesEnums` implementing `IErrorCodesEnums`.
    """

    return LoggerConfigEnums()
