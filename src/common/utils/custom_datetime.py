from datetime import UTC, datetime

import pytz

from src.common.interfaces.utils import ICustomDateTime
from src.config.settings import Settings


class CustomDateTime(ICustomDateTime):
    """
    A utility class for working with datetime objects.

    Provides methods to retrieve the current datetime either in a naive
    (timezone-unaware) form or in a timezone-aware form based on the application's
    configuration.
    """

    def __init__(
        self,
        settings: Settings,
    ):
        """
        Initializes CustomDateTime with application settings.

        :param settings: Application configuration settings.
        """

        self._settings = settings

    @staticmethod
    def get_datetime() -> datetime:
        """
        Get the current datetime without microseconds.

        This method returns the current datetime in the system's local timezone,
        without including the microsecond part.

        :return: A naive datetime object representing the current time (no timezone).
        """

        return datetime.now().replace(microsecond=0)

    @staticmethod
    def get_utc_datetime() -> datetime:
        """
        Get the current UTC datetime without microseconds.

        This method returns the current datetime in the system's local timezone,
        without including the microsecond part.

        :return: A naive datetime object representing the current time (no timezone).
        """

        return datetime.now(UTC).replace(microsecond=0).replace(tzinfo=None)

    def get_datetime_w_timezone(self) -> datetime:
        """
        Get the current datetime with timezone awareness.

        This method returns the current datetime localized to the timezone
        specified in the application's settings. The timezone is based on the
        `settings.postgres.TZ` configuration.

        :return: A timezone-aware datetime object.
        """

        return (
            datetime.now()
            .replace(microsecond=0)
            .astimezone(pytz.timezone(self._settings.project.TZ))
        )
