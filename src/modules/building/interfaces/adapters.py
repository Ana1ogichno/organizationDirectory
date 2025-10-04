from abc import ABC, abstractmethod

from sqlalchemy.sql.base import ExecutableOption

from src.common.interfaces import IPostgresBaseRepo
from src.modules.building.models import BuildingModel
from src.modules.building.schemas import BuildingCreate, BuildingUpdate


class IBuildingPsqlRepo(
    IPostgresBaseRepo[BuildingModel, BuildingCreate, BuildingUpdate], ABC
):
    """
    Interface for a repository managing building entities in PostgreSQL.

    Defines the contract for classes responsible for CRUD operations and
    business logic related to building data in the database.
    """

    @abstractmethod
    async def get_by_address_and_location(
        self,
        address: str,
        latitude: float,
        longitude: float,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> BuildingModel:
        """
        Abstract method to retrieve a building by its address and geographic coordinates.

        :param address: The building's address as a string.
        :param latitude: Latitude coordinate of the building.
        :param longitude: Longitude coordinate of the building.
        :param custom_options: Optional tuple of SQLAlchemy execution options.
        :return: BuildingModel instance matching the specified address and location.
        """
        ...
