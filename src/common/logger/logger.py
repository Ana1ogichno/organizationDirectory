import logging
import sys

from src.common.interfaces import ILoggerManager
from src.common.logger.constants import (
    LoggerConfig,
    LoggerConfigEnum,
    LoggerConfigEnums,
)


class LoggerManager(ILoggerManager):
    """
    Centralized logger manager that provides configured loggers
    based on predefined configuration enums.

    Each logger is configured once and cached for reuse.
    """

    def __init__(
        self,
        config: LoggerConfigEnums,
    ):
        """
        Initialize the LoggerManager with a logger configuration provider.

        :param config: Implementation of ILoggerConfigEnums with format, level, and
                name enums.
        """
        self._config = config
        self._loggers: dict[str, logging.Logger] = {}

    @staticmethod
    def _configure_logger(logger: logging.Logger, level: str, fmt: str) -> None:
        """
        Set up logging configuration for a logger instance.

        :param logger: Logger instance to configure.
        :param level: Logging level (e.g., 'INFO', 'DEBUG').
        :param fmt: Format string for log messages.
        """
        logger.setLevel(level)
        logger.propagate = False

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(console_handler)

    def _get_logger(self, config: LoggerConfig) -> logging.Logger:
        """
        Retrieve a logger instance based on the provided configuration.
        If the logger has not been created yet, it will be configured and cached.

        :param config: Logger configuration containing name, level, and format.
        :return: A configured and cached logger instance.
        """
        if config.name in self._loggers:
            return self._loggers[config.name]

        logger = logging.getLogger(config.name)
        if not logger.hasHandlers():
            self._configure_logger(logger, config.level, config.format)

        self._loggers[config.name] = logger
        return logger

    def get_base_logger(self) -> logging.Logger:
        """
        Get logger for base-level application logs.

        :return: Logger configured for general application base logs.
        """

        return self._get_logger(LoggerConfigEnum.BASE.value)

    def get_building_logger(self) -> logging.Logger:
        """
        Get logger specifically configured for building-related logs.

        :return: Logger configured for building module logs.
        """

        return self._get_logger(LoggerConfigEnum.BUILDING.value)

    def get_activity_logger(self) -> logging.Logger:
        """
        Get logger specifically configured for activity-related logs.

        :return: Logger configured for activity module logs.
        """

        return self._get_logger(LoggerConfigEnum.ACTIVITY.value)

    def get_organization_logger(self) -> logging.Logger:
        """
        Get logger specifically configured for organization-related logs.

        :return: Logger configured for organization module logs.
        """

        return self._get_logger(LoggerConfigEnum.ORGANIZATION.value)
