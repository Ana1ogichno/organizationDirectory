from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class BuildingBase(CoreSchema):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


@partial_schema
class BuildingUpdate(BuildingBase):
    pass


class Building(BuildingBase):
    sid: UUID
