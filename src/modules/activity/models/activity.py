from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.client.storages.postgres.core import PostgresSchemas
from src.client.storages.postgres.utils import table_args
from src.common.models import CoreModel

if TYPE_CHECKING:
    from src.modules.organization.models import OrganizationModel


class ActivityModel(CoreModel):
    __table_args__ = table_args(schema=PostgresSchemas.ACTIVITY)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(250), nullable=False, index=True)
    parent_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{PostgresSchemas.ACTIVITY}.activity.sid"), nullable=True
    )

    parent: Mapped["ActivityModel"] = relationship(
        "ActivityModel", remote_side=[sid], backref="children"
    )

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        "OrganizationModel",
        secondary=f"{PostgresSchemas.ORGANIZATION}.organization_activity",
        back_populates="activities",
    )
