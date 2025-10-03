from typing import Annotated

from fastapi import Depends

from src.client.storages.postgres.init.constants import PostgresInitEnums
from src.modules.equipments.constants import EquipmentEnums
from src.modules.equipments.constants.deps import get_equipment_common_enums
from src.modules.user.constants import UserEnums
from src.modules.user.constants.deps import get_user_common_enums


async def get_postgres_init_enums(
    user_common_enums: Annotated[UserEnums, Depends(get_user_common_enums)],
    equipment_common_enums: Annotated[
        EquipmentEnums, Depends(get_equipment_common_enums)
    ],
) -> PostgresInitEnums:
    """
    Dependency provider for PostgresInitEnums.

    This function prepares and returns an instance of PostgresInitEnums, which
    encapsulates all enum definitions required during PostgreSQL initialization.

    :param user_common_enums: Enum group with constants used in user-related setup logic
    :param equipment_common_enums: Enum group with constants used in equipment-related setup logic
    :return: An instance of PostgresInitEnums containing initialization-related enums
    """

    return PostgresInitEnums(
        user_common_enums=user_common_enums,
        equipment_common_enums=equipment_common_enums,
    )
