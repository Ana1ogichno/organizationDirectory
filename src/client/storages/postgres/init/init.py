import logging
from typing import TYPE_CHECKING, cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.client.storages.postgres.init.constants import InitCosts
from src.client.storages.postgres.interfaces import IPostgresInitializer
from src.config.settings import Settings
from src.modules.activity.interfaces import IActivityPsqlRepo
from src.modules.activity.schemas import ActivityCreate
from src.modules.building.interfaces import IBuildingPsqlRepo
from src.modules.organization.interfaces import (
    IOrganizationActivityPsqlRepo,
    IOrganizationAddressPsqlRepo,
    IOrganizationPsqlRepo,
    IPhoneNumberPsqlRepo,
)
from src.modules.organization.schemas import (
    OrganizationActivityCreate,
    OrganizationAddressCreate,
    OrganizationCreate,
    PhoneNumberCreate,
)

if TYPE_CHECKING:
    from uuid import UUID

# Configure logging
logging.basicConfig(level=logging.INFO)


class PostgresInitializer(IPostgresInitializer):
    """Initializer for populating PostgreSQL database with initial data."""

    def __init__(
        self,
        db: AsyncSession,
        consts: InitCosts,
        settings: Settings,
        building_psql_repo: IBuildingPsqlRepo,
        activity_psql_repo: IActivityPsqlRepo,
        phone_number_psql_repo: IPhoneNumberPsqlRepo,
        organization_psql_repo: IOrganizationPsqlRepo,
        organization_address_psql_repo: IOrganizationAddressPsqlRepo,
        organization_activity_psql_repo: IOrganizationActivityPsqlRepo,
    ):
        """
        Initialize the PostgresInitializer.

        :param db: AsyncSession instance.
        :param consts: InitCosts constants with initial data.
        :param settings: Application settings.
        :param building_psql_repo: Repository for building entities.
        :param activity_psql_repo: Repository for activity entities.
        :param phone_number_psql_repo: Repository for phone numbers.
        :param organization_psql_repo: Repository for organizations.
        :param organization_address_psql_repo: Repository for organization addresses.
        :param organization_activity_psql_repo: Repository for organization activities.
        """

        self._db = db
        self._consts = consts
        self._logger = logging.getLogger(__name__)
        self._settings = settings
        self._building_psql_repo = building_psql_repo
        self._activity_psql_repo = activity_psql_repo
        self._phone_number_psql_repo = phone_number_psql_repo
        self._organization_psql_repo = organization_psql_repo
        self._organization_address_psql_repo = organization_address_psql_repo
        self._organization_activity_psql_repo = organization_activity_psql_repo

    async def _create_buildings(self) -> None:
        """Create initial building records if they don't exist."""

        for building_init in self._consts.Building.BUILDINGS_FOR_INIT:
            building = await self._building_psql_repo.get_by_address_and_location(
                address=building_init.address,
                latitude=building_init.latitude,
                longitude=building_init.longitude,
            )

            if building:
                self._logger.info(
                    "Building by address %s already exist.", building_init.address
                )
            else:
                await self._building_psql_repo.create(
                    obj_in=building_init, with_commit=True
                )
                self._logger.info(
                    "Building by address %s created", building_init.address
                )

    async def _create_activity(self) -> None:
        """Create initial activities if they don't exist."""

        for activity_init in self._consts.Activity.ACTIVITIES_FOR_INIT:
            activity = await self._activity_psql_repo.get_by_name(
                name=activity_init.name
            )

            if activity:
                self._logger.info("Activity %s already exist.", activity_init.name)
            else:
                activity_in = ActivityCreate(name=activity_init.name)

                if activity_init.parent_name:
                    activity_in.parent_sid = (
                        await self._activity_psql_repo.get_by_name(
                            name=activity_init.parent_name
                        )
                    ).sid

                await self._activity_psql_repo.create(
                    obj_in=activity_in, with_commit=True
                )
                self._logger.info("Activity %s created", activity_init.name)

    async def _create_organizations(self) -> None:
        """
        Create initial organizations with phones, addresses, and activities if they
        don't exist.
        """

        for organization_init in self._consts.Organization.ORGANIZATIONS_FOR_INIT:
            organization = await self._organization_psql_repo.get_by_name(
                name=organization_init.name
            )

            if organization:
                self._logger.info(
                    "Organization %s already exist.", organization_init.name
                )
            else:
                organization = await self._organization_psql_repo.create(
                    obj_in=OrganizationCreate(name=organization_init.name),
                    with_commit=True,
                )
                self._logger.info("Organization %s created", organization_init.name)

            org_sid: UUID = cast("UUID", organization.sid)

            for phone in organization_init.phones:
                if await self._phone_number_psql_repo.get_by_organization_and_phone(
                    organization_sid=org_sid, phone=phone
                ):
                    self._logger.info(
                        "Organization %s phone %s already exist.",
                        organization_init.name,
                        phone,
                    )
                else:
                    await self._phone_number_psql_repo.create(
                        obj_in=PhoneNumberCreate(
                            organization_sid=org_sid,
                            phone=phone,
                        ),
                        with_commit=True,
                    )

                    self._logger.info(
                        "Organization %s phone %s created",
                        organization_init.name,
                        phone,
                    )

            building = await self._building_psql_repo.get_by_address_and_location(
                address=organization_init.address,
                latitude=organization_init.latitude,
                longitude=organization_init.longitude,
            )

            if await self._organization_address_psql_repo.get_by_organization_and_building_sids(
                organization_sid=org_sid,
                building_sid=building.sid,
            ):
                self._logger.info(
                    "Organization %s address already exist.", organization_init.name
                )

            else:
                await self._organization_address_psql_repo.create(
                    obj_in=OrganizationAddressCreate(
                        organization_sid=org_sid,
                        building_sid=building.sid,
                        office=organization_init.office,
                    ),
                )

                self._logger.info(
                    "Organization %s address created", organization_init.name
                )

            activity = await self._activity_psql_repo.get_by_name(
                name=organization_init.activity_name
            )

            if await self._organization_activity_psql_repo.get_by_organization_and_activity_sids(
                organization_sid=org_sid,
                activity_sid=activity.sid,
            ):
                self._logger.info(
                    "Organization %s activity already exist.", organization_init.name
                )

            else:
                await self._organization_activity_psql_repo.create(
                    obj_in=OrganizationActivityCreate(
                        organization_sid=org_sid,
                        activity_sid=activity.sid,
                    ),
                    with_commit=True,
                )

                self._logger.info(
                    "Organization %s activity created", organization_init.name
                )

    async def init(self) -> None:
        """Initializes the database with buildings, activities, and organizations."""

        await self._create_buildings()
        await self._create_activity()
        await self._create_organizations()
