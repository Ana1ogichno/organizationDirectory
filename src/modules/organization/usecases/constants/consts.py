from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from src.modules.organization.models import OrganizationAddressModel, OrganizationModel


class CustomOptions:
    """
    Provides custom SQLAlchemy query options for organization-related queries.
    """

    @staticmethod
    def full() -> list[ExecutableOption]:
        return [
            selectinload(OrganizationModel.address).selectinload(
                OrganizationAddressModel.building
            ),
            selectinload(OrganizationModel.activities),
            selectinload(OrganizationModel.phone_numbers),
        ]


class OrganizationUCConsts:
    """Constants holder class for Organization Use Case options."""

    def __init__(
        self,
    ):
        """Initializes the OrganizationUCConsts."""

        self.Options = CustomOptions
