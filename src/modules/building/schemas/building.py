from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema
from src.modules.organization.schemas import AddressWithOrganization


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


class BuildingWithOrganizations(Building):
    addresses: list[AddressWithOrganization]
