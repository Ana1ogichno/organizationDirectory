from src.config.settings import Settings


def get_settings() -> Settings:
    """
    Provides an instance of the application settings.

    :return: Settings instance with configuration loaded.
    """

    return Settings()
