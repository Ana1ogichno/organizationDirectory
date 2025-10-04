from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.client.storages.postgres.core import PostgresSchemas
from src.client.storages.postgres.utils import table_args
from src.common.models import CoreModel

if TYPE_CHECKING:
    from src.modules.organization.models import OrganizationAddressModel


class BuildingModel(CoreModel):
    __table_args__ = table_args(schema=PostgresSchemas.BUILDING)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    address: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    addresses: Mapped[list["OrganizationAddressModel"]] = relationship(
        "OrganizationAddressModel", back_populates="building"
    )
