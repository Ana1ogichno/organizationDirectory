from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from src.modules.building.models import BuildingModel
from src.modules.organization.models import OrganizationAddressModel


class CustomOptions:
    """
    Provides custom SQLAlchemy query options for building-related queries.
    """

    @staticmethod
    def with_organizations() -> list[ExecutableOption]:
        """
        Returns a list of SQLAlchemy options to eagerly load building addresses
        along with their associated organizations.

        :return: List of ExecutableOption for query customization.
        """

        return [
            selectinload(BuildingModel.addresses).selectinload(
                OrganizationAddressModel.organization
            )
        ]


class BuildingUCConsts:
    """Constants holder class for Building Use Case options."""

    def __init__(
        self,
    ):
        """Initializes the BuildingUCConsts."""

        self.Options = CustomOptions
