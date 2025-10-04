from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.client.storages.postgres.core import PostgresSchemas
from src.client.storages.postgres.utils import table_args
from src.common.models import CoreModel

if TYPE_CHECKING:
    from src.modules.activity.models import ActivityModel
    from src.modules.building.models import BuildingModel


class OrganizationModel(CoreModel):
    __table_args__ = table_args(schema=PostgresSchemas.ORGANIZATION)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(250), nullable=False, index=True)

    phone_numbers: Mapped[list["PhoneNumberModel"]] = relationship(
        "PhoneNumberModel", back_populates="organization"
    )
    address: Mapped["OrganizationAddressModel"] = relationship(
        "OrganizationAddressModel", back_populates="organization"
    )
    activities: Mapped["ActivityModel"] = relationship(
        "ActivityModel",
        secondary=f"{PostgresSchemas.ORGANIZATION}.organization_activity",
        back_populates="organizations",
    )


class PhoneNumberModel(CoreModel):
    __table_args__ = table_args(schema=PostgresSchemas.ORGANIZATION)

    sid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{PostgresSchemas.ORGANIZATION}.organization.sid"), nullable=False
    )
    phone: Mapped[str] = mapped_column(String(25), nullable=False)

    organization: Mapped["OrganizationModel"] = relationship(
        "OrganizationModel", back_populates="phone_numbers"
    )


class OrganizationAddressModel(CoreModel):
    __table_args__ = table_args(schema=PostgresSchemas.ORGANIZATION)

    organization_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{PostgresSchemas.ORGANIZATION}.organization.sid"), primary_key=True
    )
    building_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{PostgresSchemas.BUILDING}.building.sid"), primary_key=True
    )
    office: Mapped[str] = mapped_column(String(25), nullable=True)

    organization: Mapped["OrganizationModel"] = relationship(
        "OrganizationModel", back_populates="address"
    )
    building: Mapped["BuildingModel"] = relationship(
        "BuildingModel", back_populates="addresses"
    )


class OrganizationActivityModel(CoreModel):
    __table_args__ = table_args(schema=PostgresSchemas.ORGANIZATION)

    organization_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{PostgresSchemas.ORGANIZATION}.organization.sid"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    activity_sid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{PostgresSchemas.ACTIVITY}.activity.sid"),
        primary_key=True,
        nullable=False,
        index=True,
    )
