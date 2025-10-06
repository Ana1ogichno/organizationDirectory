from datetime import datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from src.common.utils import CustomDateTime


class CoreModel(DeclarativeBase):
    sid: Any

    created_at: Mapped[datetime] = mapped_column(
        DateTime(), default=CustomDateTime.get_utc_datetime
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=CustomDateTime.get_utc_datetime,
        onupdate=CustomDateTime.get_utc_datetime,
    )

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__.replace("Model", "")
        res = [name[0].lower()]
        for c in name[1:]:
            if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                res.append("_")
                res.append(c.lower())
            else:
                res.append(c)
        cls.__name__ = "".join(res)
        return cls.__name__
