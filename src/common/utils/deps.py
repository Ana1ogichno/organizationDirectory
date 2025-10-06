from typing import Annotated

from fastapi import Depends

from src.common.interfaces import ICustomDateTime
from src.common.utils import CustomDateTime
from src.config.settings import Settings
from src.config.settings.deps import get_settings


def get_custom_datetime(
    settings: Annotated[Settings, Depends(get_settings)],
) -> ICustomDateTime:
    """
    Provides an instance of CustomDateTime configured with application settings.

    :param settings: Application settings dependency.
    :return: Configured CustomDateTime instance implementing ICustomDateTime.
    """

    return CustomDateTime(
        settings=settings,
    )
