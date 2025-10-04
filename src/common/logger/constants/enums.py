from dataclasses import dataclass
from enum import Enum, StrEnum

from src.config.settings.deps import get_settings


@dataclass(frozen=True)
class LoggerConfig:
    name: str
    level: str
    format: str


class LoggerFormatEnum(StrEnum):
    """Defines different formats for logging."""

    BASE = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) %(message)s"


class LoggerLevelEnum(StrEnum):
    """Defines the available log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerNameEnum(StrEnum):
    """Defines predefined logger names."""

    BASE = "BASE"
    BUILDING = "BUILDING"
    ACTIVITY = "ACTIVITY"
    ORGANIZATION = "ORGANIZATION"


class LoggerConfigEnum(Enum):
    """Centralized container for logger configuration presets."""

    BASE = LoggerConfig(
        LoggerNameEnum.BASE,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )

    BUILDING = LoggerConfig(
        LoggerNameEnum.BUILDING,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )

    ACTIVITY = LoggerConfig(
        LoggerNameEnum.ACTIVITY,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )

    ORGANIZATION = LoggerConfig(
        LoggerNameEnum.ORGANIZATION,
        get_settings().project.LOG_LEVEL.upper(),
        LoggerFormatEnum.BASE,
    )


class LoggerConfigEnums:
    """
    Centralized container for all grouped logger-related enums.
    """

    Format: type[LoggerFormatEnum] = LoggerFormatEnum
    Level: type[LoggerLevelEnum] = LoggerLevelEnum
    Name: type[LoggerNameEnum] = LoggerNameEnum
    Config: type[LoggerConfigEnum] = LoggerConfigEnum
