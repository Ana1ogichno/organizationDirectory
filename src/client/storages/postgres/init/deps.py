from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.deps import (
    get_redis_client,
    get_redis_session_provider,
    get_s3_session_provider,
)
from src.client.storages.postgres.init import PostgresInitializer
from src.client.storages.postgres.init.constants.deps import get_postgres_init_enums
from src.client.storages.postgres.interfaces import IPostgresInitializer
from src.client.storages.s3.core.deps import get_s3_client
from src.client.web.deps import (
    get_appeal_client,
    get_appeal_client_provider,
    get_association_client,
    get_association_client_provider,
    get_auth_client,
    get_auth_client_provider,
)
from src.common.constants.deps import get_common_enums, get_error_codes
from src.common.helpers.deps import get_password_helper
from src.common.logger.constants.deps import get_logger_config
from src.common.logger.deps import get_logger_manager, get_user_logger
from src.config.settings.deps import get_settings
from src.modules.equipments.adapters.repositories.deps import (
    get_equipment_property_type_pg_repo,
    get_equipment_type_pg_repo,
)
from src.modules.equipments.constants.deps import get_equipment_common_enums
from src.modules.user.adapters.repositories.postgres.deps import (
    get_notification_postgres_repo,
    get_privacy_postgres_repo,
    get_status_postgres_repo,
    get_user_postgres_repo,
    get_user_statuses_postgres_repo,
)
from src.modules.user.adapters.repositories.redis.deps import get_user_redis_repo
from src.modules.user.adapters.repositories.s3.deps import get_user_s3_repo
from src.modules.user.adapters.web.constants.deps import get_user_web_adp_enums
from src.modules.user.adapters.web.deps import (
    get_appeal_web_adp,
    get_association_web_adp,
    get_user_auth_web_adp,
)
from src.modules.user.constants.deps import get_user_common_enums
from src.modules.user.services.constants.deps import (
    get_user_srv_consts,
    get_user_srv_enums,
)
from src.modules.user.services.deps import get_user_service


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

    session_provider = await get_redis_session_provider(settings=get_settings())

    redis_gen = get_redis_client(session_provider=session_provider)

    redis = await anext(redis_gen)

    logger = get_user_logger(get_logger_manager(get_logger_config()))
    error_codes = get_error_codes()
    password_helper = get_password_helper()
    user_postgres_repo = await get_user_postgres_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    privacy_postgres_repo = await get_privacy_postgres_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    notification_postgres_repo = await get_notification_postgres_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    settings = get_settings()
    s3_session_provider = await get_s3_session_provider(
        s3_client=await get_s3_client(settings=settings)
    )
    user_statuses_postgres_repo = await get_user_statuses_postgres_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    user_common_enums = get_user_common_enums()
    equipment_type_postgres_repo = await get_equipment_type_pg_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    equipment_property_type_postgres_repo = await get_equipment_property_type_pg_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    equipment_common_enums = get_equipment_common_enums()
    status_postgres_repo = await get_status_postgres_repo(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )
    user_auth_web_adp = await get_user_auth_web_adp(
        enums=get_user_web_adp_enums(),
        client=get_auth_client(
            auth_client_provider=get_auth_client_provider(settings=settings)
        ),
        logger=logger,
        error_codes=error_codes,
    )
    association_web_adp = await get_association_web_adp(
        enums=get_user_web_adp_enums(),
        client=get_association_client(
            association_client_provider=get_association_client_provider(
                settings=settings
            )
        ),
        logger=logger,
        error_codes=error_codes,
    )
    user_service = await get_user_service(
        db=db,
        enums=get_user_srv_enums(
            common_enums=get_common_enums(), user_common_enums=user_common_enums
        ),
        consts=get_user_srv_consts(),
        logger=logger,
        settings=settings,
        user_s3_repo=await get_user_s3_repo(
            logger=logger, s3_session_provider=s3_session_provider
        ),
        error_codes=error_codes,
        appeal_web_adp=await get_appeal_web_adp(
            enums=get_user_web_adp_enums(),
            client=get_appeal_client(
                appeal_client_provider=get_appeal_client_provider(settings=settings)
            ),
            logger=logger,
            error_codes=error_codes,
        ),
        password_helper=password_helper,
        user_redis_repo=await get_user_redis_repo(
            redis=redis,
            logger=logger,
            error_codes=error_codes,
        ),
        user_auth_web_adp=user_auth_web_adp,
        user_postgres_repo=user_postgres_repo,
        status_postgres_repo=status_postgres_repo,
        user_statuses_postgres_repo=user_statuses_postgres_repo,
        association_web_adp=association_web_adp,
    )

    return PostgresInitializer(
        db=db,
        enums=await get_postgres_init_enums(
            user_common_enums=user_common_enums,
            equipment_common_enums=equipment_common_enums,
        ),
        settings=settings,
        user_service=user_service,
        user_postgres_repo=user_postgres_repo,
        status_postgres_repo=status_postgres_repo,
        privacy_postgres_repo=privacy_postgres_repo,
        notification_postgres_repo=notification_postgres_repo,
        user_statuses_postgres_repo=user_statuses_postgres_repo,
        equipment_type_postgres_repo=equipment_type_postgres_repo,
        equipment_property_type_postgres_repo=equipment_property_type_postgres_repo,
    )
