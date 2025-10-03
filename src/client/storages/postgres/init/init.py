import logging
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.postgres.init.constants import PostgresInitEnums
from src.client.storages.postgres.interfaces import IPostgresInitializer
from src.config.settings import Settings
from src.modules.equipments.interfaces import (
    IEquipmentPropertyTypePostgresRepo,
    IEquipmentTypePostgresRepo,
)
from src.modules.equipments.schemas import (
    EquipmentPropertyTypeCreate,
    EquipmentTypeCreate,
)
from src.modules.user.interfaces import (
    INotificationPostgresRepo,
    IPrivacyPostgresRepo,
    IStatusPostgresRepo,
    IUserPostgresRepo,
    IUserSrv,
    IUserStatusesPostgresRepo,
)
from src.modules.user.models import UserModel
from src.modules.user.schemas import (
    ClientUserCreate,
    NotificationCreate,
    PrivacyCreate,
    StatusCreate,
    UserStatusesCreate,
)

# Configure logging
logging.basicConfig(level=logging.INFO)


class PostgresInitializer(IPostgresInitializer):
    """
    Handles database initialization including creation of initial data like superusers.

    This class provides methods to initialize database state and ensure required system
    data exists.
    """

    def __init__(
        self,
        db: AsyncSession,
        enums: PostgresInitEnums,
        settings: Settings,
        user_service: IUserSrv,
        user_postgres_repo: IUserPostgresRepo,
        status_postgres_repo: IStatusPostgresRepo,
        privacy_postgres_repo: IPrivacyPostgresRepo,
        notification_postgres_repo: INotificationPostgresRepo,
        user_statuses_postgres_repo: IUserStatusesPostgresRepo,
        equipment_type_postgres_repo: IEquipmentTypePostgresRepo,
        equipment_property_type_postgres_repo: IEquipmentPropertyTypePostgresRepo,
    ):
        """
        Initializes the PostgresInitializer with required dependencies.

        :param db: Scoped asynchronous session for database operations
        :param enums: Container with enums required for initialization
        :param settings: Application settings object
        :param user_service: Service responsible for user operations
        :param user_postgres_repo: PostgreSQL repository for user entity
        :param status_postgres_repo: PostgreSQL repository for status entity
        :param privacy_postgres_repo: PostgreSQL repository for privacy settings
        :param notification_postgres_repo: PostgreSQL repository for notification
                settings
        :param user_statuses_postgres_repo: Repository for user-status relationships in
                PostgreSQL.
        """

        self._db = db
        self._enums = enums
        self._logger = logging.getLogger(__name__)
        self._settings = settings
        self._user_service = user_service
        self._user_postgres_repo = user_postgres_repo
        self._status_postgres_repo = status_postgres_repo
        self._privacy_postgres_repo = privacy_postgres_repo
        self._notification_postgres_repo = notification_postgres_repo
        self._user_statuses_postgres_repo = user_statuses_postgres_repo
        self._equipment_type_postgres_repo = equipment_type_postgres_repo
        self._equipment_property_type_postgres_repo = (
            equipment_property_type_postgres_repo
        )

    async def _create_status(self, name: str) -> None:
        status = await self._status_postgres_repo.get_by_name(name=name)

        if status:
            self._logger.info("Status %s already exist.", name)
        else:
            status_in = StatusCreate(name=name)
            await self._status_postgres_repo.create(obj_in=status_in, with_commit=False)
            self._logger.info("Status created: %s", name)

    async def _create_superuser(self, email: EmailStr, password: str) -> UserModel:
        """
        Creates a new superuser with provided credentials in the database.

        :param email: Email address for the new superuser
        :param password: Password for the new superuser
        """

        user = await self._user_postgres_repo.get_by_email(email=email)

        if user:
            self._logger.info("Superuser already exist.")
        else:
            user_in = ClientUserCreate(
                email=email, password=password, nickname="superuser", name="estesis"
            )
            user = await self._user_service.create_user(
                user_in=user_in, with_commit=True
            )
            self._logger.info("Superuser created: %s", email)

        return user

    async def _create_superuser_permission(
        self, user_sid: UUID, status_name: str
    ) -> None:
        status = await self._status_postgres_repo.get_by_name(name=status_name)

        if not await self._user_statuses_postgres_repo.get_by_status_sid_and_user_sid(
            user_sid=user_sid, status_sid=status.sid
        ):
            user_status_in = UserStatusesCreate(
                user_sid=user_sid, status_sid=status.sid
            )
            await self._user_statuses_postgres_repo.create(
                obj_in=user_status_in, with_commit=False
            )
            self._logger.info("Add status %s for superuser", status_name)

    async def _create_privacy(self, name: str, privacy_id: int) -> None:
        """
        Creates a privacy option if it does not already exist.

        This method checks if a privacy record with the given name exists.
        If not, it creates a new privacy entry in the database.

        :param name: The name of the privacy setting to ensure exists
        :param privacy_id: The id of the privacy setting to ensure exists
        """

        privacy = await self._privacy_postgres_repo.get_by_name(name=name)

        if privacy:
            self._logger.info("Privacy %s already exist.", name)
        else:
            privacy_in = PrivacyCreate(name=name, id=privacy_id)
            await self._privacy_postgres_repo.create(obj_in=privacy_in)
            self._logger.info("Privacy created: %s", name)

    async def _create_notification(self, name: str, notification_id: int) -> None:
        """
        Creates a notification type if it does not already exist.

        This method checks if a notification record with the given name exists.
        If not, it creates a new notification entry in the database.

        :param name: The name of the notification type to ensure exists
        :param notification_id: The id of the notification setting to ensure exists
        """

        notification = await self._notification_postgres_repo.get_by_name(name=name)

        if notification:
            self._logger.info("Notification %s already exist.", name)
        else:
            notification_in = NotificationCreate(name=name, id=notification_id)
            await self._notification_postgres_repo.create(obj_in=notification_in)
            self._logger.info("Notification created: %s", name)

    async def _create_equipment_type(self, name: str, equipment_type_id: int) -> None:
        """
        Creates equipment type if it does not already exist.

        This method checks if equipment record with the given name exists.
        If not, it creates a new equipment entry in the database.

        :param name: The name of the equipment type to ensure exists
        :param equipment_type_id: The id of the equipment to ensure exists
        """

        equipment = await self._equipment_type_postgres_repo.get_by_name(name=name)

        if equipment:
            self._logger.info("Equipment %s already exist.", name)
        else:
            equipment_in = EquipmentTypeCreate(name=name, id=equipment_type_id)
            await self._equipment_type_postgres_repo.create(obj_in=equipment_in)
            self._logger.info("Equipment created: %s", name)

    async def _create_equipment_property_type(
        self, name: str, equipment_property_type_id: int
    ) -> None:
        """
        Creates equipment property type if it does not already exist.

        This method checks if equipment property record with the given name exists.
        If not, it creates a new equipment property entry in the database.

        :param name: The name of the equipment property type to ensure exists
        :param equipment_property_type_id: The id of the equipment property to ensure exists
        """

        equipment_property = (
            await self._equipment_property_type_postgres_repo.get_by_name(name=name)
        )

        if equipment_property:
            self._logger.info("Equipment property %s already exist.", name)
        else:
            equipment_property_in = EquipmentPropertyTypeCreate(
                name=name, id=equipment_property_type_id
            )
            await self._equipment_property_type_postgres_repo.create(
                obj_in=equipment_property_in
            )
            self._logger.info("Equipment property created: %s", name)

    async def _init_pg_trgm(self) -> None:
        """
        Initializes the PostgreSQL pg_trgm extension if it is not already installed.

        This extension provides functions and operators for trigram matching,
        which can improve text search performance.
        """

        self._logger.info("Starting pg_trgm initialization")

        await self._db.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        await self._db.commit()

        self._logger.info("Completed pg_trgm initialization")

    async def _init_statuses(self) -> None:
        """Initializes the default statuses if it doesn't exist."""

        self._logger.info("Starting statuses initialization")

        for status in self._enums.User.Status:
            await self._create_status(name=status)

        await self._db.commit()

        self._logger.info("Completed statuses initialization")

    async def _init_superuser(self) -> None:
        """Initializes the default superuser account if it doesn't exist."""

        email = self._settings.project.FIRST_SUPERUSER_LOGIN
        password = self._settings.project.FIRST_SUPERUSER_PASSWORD

        self._logger.info("Starting superuser initialization")

        user = await self._create_superuser(email, password)
        for status in self._enums.User.Status:
            await self._db.refresh(user)
            await self._create_superuser_permission(
                user_sid=user.sid, status_name=status
            )

        await self._db.flush()

        self._logger.info("Completed superuser initialization")

    async def _init_privacy_settings(self) -> None:
        """
        Initializes privacy settings from enum if they do not exist.

        This method iterates over predefined privacy names and ensures that
        each setting exists in the database.
        """

        self._logger.info("Starting privacy initialization")

        for privacy in self._enums.User.Privacy:
            await self._create_privacy(name=privacy.name, privacy_id=privacy.value)

        await self._db.commit()

        self._logger.info("Completed privacy initialization")

    async def _init_notification_settings(self) -> None:
        """
        Initializes notification settings from enum if they do not exist.

        This method iterates over predefined notification types and ensures that
        each type exists in the database.
        """

        self._logger.info("Starting notification initialization")

        for notification in self._enums.User.Notification:
            await self._create_notification(
                name=notification.name, notification_id=notification.value
            )

        await self._db.commit()

        self._logger.info("Completed notification initialization")

    async def _init_equipment_types(self) -> None:
        """
        Initializes equipment type from enum if they do not exist.

        This method iterates over predefined equipment types and ensures that
        each type exists in the database.
        """

        self._logger.info("Starting equipment type initialization")

        for equipment_type in self._enums.Equipment.EquipmentType:
            await self._create_equipment_type(
                name=equipment_type.name, equipment_type_id=equipment_type.value
            )

        await self._db.commit()

        self._logger.info("Completed equipment type initialization")

    async def _init_equipment_property_types(self) -> None:
        """
        Initializes equipment property type from enum if they do not exist.

        This method iterates over predefined equipment property types and ensures that
        each type exists in the database.
        """

        self._logger.info("Starting equipment property type initialization")

        for equipment_property_type in self._enums.Equipment.EquipmentPropertyType:
            await self._create_equipment_property_type(
                name=equipment_property_type.name,
                equipment_property_type_id=equipment_property_type.value,
            )

        await self._db.commit()

        self._logger.info("Completed equipment property type initialization")

    async def init(self) -> None:
        """
        Initialize application data by setting up the superuser,
        privacy settings, and notification settings.
        """

        await self._init_pg_trgm()
        await self._init_statuses()
        await self._init_superuser()
        await self._init_equipment_types()
        await self._init_privacy_settings()
        await self._init_notification_settings()
        await self._init_equipment_property_types()
