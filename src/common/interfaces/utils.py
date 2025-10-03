from abc import ABC, abstractmethod
from datetime import datetime


class ICustomDateTime(ABC):
    """
    Interface for datetime utilities.

    Provides methods to obtain the current datetime in either naive
    (timezone-unaware) or timezone-aware form, depending on application requirements.
    """

    @staticmethod
    @abstractmethod
    def get_datetime() -> datetime:
        """
        Get the current datetime without microseconds.

        :return: Naive datetime object (without timezone).
        """
        ...

    @staticmethod
    @abstractmethod
    def get_utc_datetime() -> datetime:
        """
        Get the current UTC datetime without microseconds.

        :return: Naive datetime object (without timezone).
        """

    @abstractmethod
    def get_datetime_w_timezone(self) -> datetime:
        """
        Get the current datetime with timezone awareness based on application settings.

        :return: Aware datetime object localized to the configured timezone.
        """
        ...
