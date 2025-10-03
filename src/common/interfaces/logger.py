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
        """Returns the base application logger (general-purpose logging)."""
        ...

    @abstractmethod
    def get_user_logger(self) -> logging.Logger:
        """Returns the user-specific logger for logging user-related activities."""
        ...

    @abstractmethod
    def get_status_logger(self) -> logging.Logger:
        """Returns the status-specific logger for logging status-related activities."""
        ...
