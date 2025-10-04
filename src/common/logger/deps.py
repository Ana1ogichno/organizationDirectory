import logging
from typing import Annotated

from fastapi import Depends

from src.common.interfaces import ILoggerManager
from src.common.logger import LoggerManager
from src.common.logger.constants import LoggerConfigEnums
from src.common.logger.constants.deps import get_logger_config


def get_logger_manager(
    config: Annotated[LoggerConfigEnums, Depends(get_logger_config)],
) -> LoggerManager:
    """
    Dependency provider for LoggerManager with injected configuration.

    :param config: Logger configuration enums.
    :return: Initialized LoggerManager instance.
    """
    return LoggerManager(config)


def get_base_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Retrieve the base logger instance.

    :param manager: LoggerManager instance.
    :return: Configured base logger.
    """
    return manager.get_base_logger()


def get_building_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Get logger specifically configured for building-related logs.

    :param manager: LoggerManager instance.
    :return: Logger configured for building module logs.
    """

    return manager.get_building_logger()


def get_activity_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Get logger specifically configured for activity-related logs.

    :param manager: LoggerManager instance.
    :return: Logger configured for activity module logs.
    """

    return manager.get_activity_logger()


def get_organization_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Get logger specifically configured for organization-related logs.

    :param manager: LoggerManager instance.
    :return: Logger configured for organization module logs.
    """

    return manager.get_organization_logger()
