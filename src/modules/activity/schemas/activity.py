from uuid import UUID

from src.common.decorators import partial_schema
from src.common.schemas import CoreSchema


class ActivityBase(CoreSchema):
    name: str
    parent_sid: UUID | None = None


class ActivityCreate(ActivityBase):
    pass


class ActivityInit(ActivityCreate):
    parent_name: str | None


@partial_schema
class ActivityUpdate(ActivityBase):
    pass


class Activity(ActivityBase):
    sid: UUID
