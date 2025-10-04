from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.sql.base import ExecutableOption

from src.common.interfaces import IPostgresBaseRepo
from src.modules.organization.models.organization import (
    OrganizationActivityModel,
    OrganizationAddressModel,
    OrganizationModel,
    PhoneNumberModel,
)
from src.modules.organization.schemas import (
    OrganizationActivityCreate,
    OrganizationActivityUpdate,
    OrganizationAddressCreate,
    OrganizationAddressUpdate,
    OrganizationCreate,
    OrganizationUpdate,
    PhoneNumberCreate,
    PhoneNumberUpdate,
)


class IOrganizationPsqlRepo(
    IPostgresBaseRepo[OrganizationModel, OrganizationCreate, OrganizationUpdate], ABC
):
    """
    Interface for a repository managing organizations in PostgreSQL.

    Defines the contract for classes responsible for CRUD operations
    and business logic related to organizations in the database.
    """

    @abstractmethod
    async def get_by_name(
        self, name: str, custom_options: tuple[ExecutableOption, ...] | None = None
    ) -> OrganizationModel | None:
        """
        Abstract method to retrieve an organization by its name.

        :param name: Name of the organization.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: OrganizationModel instance matching the name or None.
        """
        ...


class IPhoneNumberPsqlRepo(
    IPostgresBaseRepo[PhoneNumberModel, PhoneNumberCreate, PhoneNumberUpdate], ABC
):
    """
    Interface for a repository managing phone number entities in PostgreSQL.

    Defines the contract for classes responsible for storing, retrieving, and managing
    user phone number records in the database.
    """

    @abstractmethod
    async def get_by_organization_and_phone(
        self,
        organization_sid: UUID,
        phone: str,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> PhoneNumberModel | None:
        """
        Abstract method to retrieve a phone number by organization UUID and phone
        string.

        :param organization_sid: UUID of the organization.
        :param phone: Phone number string.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: PhoneNumberModel instance matching the criteria or None.
        """
        ...


class IOrganizationAddressPsqlRepo(
    IPostgresBaseRepo[
        OrganizationAddressModel, OrganizationAddressCreate, OrganizationAddressUpdate
    ],
    ABC,
):
    """
    Interface for a repository managing organization addresses in PostgreSQL.

    Defines the contract for classes responsible for CRUD operations and
    business logic related to organization addresses in the database.
    """

    @abstractmethod
    async def get_by_organization_and_building_sids(
        self,
        building_sid: UUID,
        organization_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> OrganizationAddressModel | None:
        """
        Abstract method to retrieve an organization address by building and
        organization UUIDs.

        :param building_sid: UUID of the building.
        :param organization_sid: UUID of the organization.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: OrganizationAddressModel instance matching the criteria or None.
        """
        ...


class IOrganizationActivityPsqlRepo(
    IPostgresBaseRepo[
        OrganizationActivityModel,
        OrganizationActivityCreate,
        OrganizationActivityUpdate,
    ],
    ABC,
):
    """
    Interface for a repository managing organization activities in PostgreSQL.

    Defines the contract for classes responsible for CRUD operations and
    business logic related to organization activities in the database.
    """

    @abstractmethod
    async def get_by_organization_and_activity_sids(
        self,
        activity_sid: UUID,
        organization_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> OrganizationActivityModel | None:
        """
        Abstract method to retrieve an organization activity by activity and
        organization UUIDs.

        :param activity_sid: UUID of the activity.
        :param organization_sid: UUID of the organization.
        :param custom_options: Optional SQLAlchemy execution options.
        :return: OrganizationActivityModel instance matching the criteria or None.
        """
        ...
