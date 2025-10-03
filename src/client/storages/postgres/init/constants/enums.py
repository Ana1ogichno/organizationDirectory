from src.modules.equipments.constants import EquipmentEnums
from src.modules.user.constants import UserEnums


class PostgresInitEnums:
    """
    Container for enums required during PostgreSQL initialization procedures.

    This class holds structured enum definitions used during the setup of essential
    system components, such as user creation, role assignment, and default
    configuration.
    """

    def __init__(
        self,
        user_common_enums: UserEnums,
        equipment_common_enums: EquipmentEnums,
    ):
        """
        Initializes the PostgresInitEnums container with required enum groups.

        :param user_common_enums: Enum group containing user-related constants
                used during initialization.
        :param equipment_common_enums: Enum group containing equipment-related constants
                used during initialization.
        """

        self.User = user_common_enums
        self.Equipment = equipment_common_enums
