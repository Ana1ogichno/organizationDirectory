import logging

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.modules.building.interfaces import IBuildingPsqlRepo
from src.modules.building.models import BuildingModel
from src.modules.building.schemas import BuildingCreate, BuildingUpdate


class BuildingPsqlRepo(
    PostgresBaseRepo[BuildingModel, BuildingCreate, BuildingUpdate],
    IBuildingPsqlRepo,
):
    """
    Repository implementation for Buildings using PostgreSQL database.
    Provides data access methods specific to Building entities.
    """

    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initializes the repository with database session, error codes, and logger.

        :param db: AsyncSession instance for database connectivity.
        :param errors: Enumeration of error codes for handling repository errors.
        :param logger: Logger instance for logging repository operations.
        """

        super().__init__(db=db, model=BuildingModel, errors=errors, logger=logger)
        self._errors = errors
        self._logger = logger

    @LoggingFunctionInfo(
        description="Retrieves a building by address and geographic coordinates."
    )
    async def get_by_address_and_location(
        self,
        address: str,
        latitude: float,
        longitude: float,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> BuildingModel:
        """
        Fetches a single building matching the specified address and geographic
        location.

        :param address: The address of the building.
        :param latitude: The latitude coordinate of the building location.
        :param longitude: The longitude coordinate of the building location.
        :param custom_options: Optional SQLAlchemy execution options
                (e.g., query hints).
        :return: BuildingModel instance matching the criteria.
        """

        self._logger.debug(
            "Fetching building at address '%s' with coordinates (%f, %f)",
            address,
            latitude,
            longitude,
        )

        query = await self._apply_options(
            query=select(self._model).where(
                and_(
                    self._model.address == address,
                    self._model.latitude == latitude,
                    self._model.longitude == longitude,
                )
            ),
            options=custom_options,
        )

        return await self._get_single_result(query)
