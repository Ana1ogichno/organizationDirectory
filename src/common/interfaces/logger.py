import logging
from abc import ABC, abstractmethod


class ILoggerManager(ABC):
    """
    Interface for a logger manager that provides access to various
    loggers used throughout the application.

    Each logger should be configured according to the project’s
    logging standards (level, format, handlers, etc.).
    """

    @abstractmethod
    def get_base_logger(self) -> logging.Logger:
        """
        Get logger for base-level application logs.

        :return: Logger configured for general application base logs.
        """
        ...

    @abstractmethod
    def get_building_logger(self) -> logging.Logger:
        """
        Get logger specifically configured for building-related logs.

        :return: Logger configured for building module logs.
        """
        ...

    @abstractmethod
    def get_activity_logger(self) -> logging.Logger:
        """
        Get logger specifically configured for activity-related logs.

        :return: Logger configured for activity module logs.
        """
        ...

    @abstractmethod
    def get_organization_logger(self) -> logging.Logger:
        """
        Get logger specifically configured for organization-related logs.

        :return: Logger configured for organization module logs.
        """
        ...
