from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.postgres.init import PostgresInitializer
from src.client.storages.postgres.init.constants.deps import get_init_consts
from src.client.storages.postgres.interfaces import IPostgresInitializer
from src.common.constants.deps import get_error_codes
from src.common.logger.constants.deps import get_logger_config
from src.common.logger.deps import (
    get_activity_logger,
    get_building_logger,
    get_logger_manager,
    get_organization_logger,
)
from src.config.settings.deps import get_settings
from src.modules.activity.adapters.repositories.postgres.deps import (
    get_activity_psql_repo,
)
from src.modules.building.adapters.repositories.postgres.deps import (
    get_building_psql_repo,
)
from src.modules.organization.adapters.repositories.postgres.deps import (
    get_organization_activity_psql_repo,
    get_organization_address_psql_repo,
    get_organization_psql_repo,
    get_phone_number_psql_repo,
)


async def get_psql_initializer(
    db: AsyncSession,
) -> IPostgresInitializer:
    """
    Provides a fully initialized PostgresInitializer instance with all dependencies.

    This factory function assembles all necessary components for database
    initialization, including logging, error handling, password utilities, and user
    services, then returns a configured PostgresInitializer instance.

    :param db: Async database session provided by the PostgresSessionProvider.
            This session will be used for all database operations during
            initialization.
    :return: Fully configured PostgresInitializer instance ready for database
            initialization tasks.
    """

    settings = get_settings()

    logger_manager = get_logger_manager(config=get_logger_config())

    errors = get_error_codes()

    return PostgresInitializer(
        db=db,
        consts=await get_init_consts(),
        settings=settings,
        building_psql_repo=await get_building_psql_repo(
            db=db,
            logger=get_building_logger(manager=logger_manager),
            error_codes=errors,
        ),
        activity_psql_repo=await get_activity_psql_repo(
            db=db,
            logger=get_activity_logger(manager=logger_manager),
            error_codes=errors,
        ),
        phone_number_psql_repo=await get_phone_number_psql_repo(
            db=db,
            logger=get_organization_logger(manager=logger_manager),
            error_codes=errors,
        ),
        organization_psql_repo=await get_organization_psql_repo(
            db=db,
            logger=get_organization_logger(manager=logger_manager),
            error_codes=errors,
        ),
        organization_address_psql_repo=await get_organization_address_psql_repo(
            db=db,
            logger=get_organization_logger(manager=logger_manager),
            error_codes=errors,
        ),
        organization_activity_psql_repo=await get_organization_activity_psql_repo(
            db=db,
            logger=get_organization_logger(manager=logger_manager),
            error_codes=errors,
        ),
    )
