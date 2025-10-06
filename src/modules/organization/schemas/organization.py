from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class OrganizationBase(CoreSchema):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


@partial_schema
class OrganizationUpdate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    sid: UUID


class OrganizationInit(OrganizationCreate):
    phones: list[str]
    address: str
    office: str
    latitude: float
    longitude: float
    activity_name: str


class PhoneNumberBase(CoreSchema):
    organization_sid: UUID
    phone: str


class PhoneNumberCreate(PhoneNumberBase):
    pass


@partial_schema
class PhoneNumberUpdate(PhoneNumberBase):
    pass


class OrganizationAddressBase(CoreSchema):
    organization_sid: UUID
    building_sid: UUID
    office: str


class OrganizationAddressCreate(OrganizationAddressBase):
    pass


@partial_schema
class OrganizationAddressUpdate(OrganizationAddressBase):
    pass


class AddressWithOrganization(OrganizationAddressBase):
    organization: Organization


class OrganizationActivityBase(CoreSchema):
    organization_sid: UUID
    activity_sid: UUID


class OrganizationActivityCreate(OrganizationActivityBase):
    pass


@partial_schema
class OrganizationActivityUpdate(OrganizationActivityBase):
    pass
