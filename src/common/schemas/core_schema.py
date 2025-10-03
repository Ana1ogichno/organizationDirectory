from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel, to_snake


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        validate_by_name = True


class CoreSchema(CamelModel):
    @field_validator("*", mode="after")
    def timezone_validate(cls, v: Any) -> Any:  # noqa: ANN401 N805
        if isinstance(v, datetime) and v.tzinfo is not None:
            v = v.replace(tzinfo=None)
        return v

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat() + "Z",
        },
        populate_by_name=True,
    )


class SQLFilterBase(Filter):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    @field_validator("order_by", mode="before", check_fields=False)
    @classmethod
    def camel_to_snake(cls, v: str | list[str]) -> list[str]:
        """
        Transform camelCase field names to snake_case in order_by parameter.

        Handles sorting field names by converting camelCase to snake_case while
        preserving sort direction indicators (+/-) at the start of field names.

        :param v: Field name(s) to transform (with optional sort direction indicators)
        :return: List of transformed field names in snake_case with preserved direction
        """
        if not v:
            return v

        if isinstance(v, str):
            v = [v]

        result = []
        for field in v:
            sign = None
            if field[0] in ["+", "-"]:
                sign = field[0]
                field_no_sign = field[1:]
            else:
                field_no_sign = field
            new_val = to_snake(field_no_sign)
            if sign is not None:
                new_val = sign + new_val
            result.append(new_val)

        return result
