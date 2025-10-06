from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from src.common.schemas import SQLFilterBase
from src.modules.building.models import BuildingModel


class BuildingCoordinatesFilter(SQLFilterBase):
    latitude__gte: float = Field(..., alias="latitudeGte")
    latitude__lte: float = Field(..., alias="latitudeLte")
    longitude__gte: float = Field(..., alias="longitudeGte")
    longitude__lte: float = Field(..., alias="longitudeLte")

    class Constants(Filter.Constants):
        model = BuildingModel
