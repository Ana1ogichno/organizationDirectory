from src.client.storages.postgres.init.constants import InitCosts


async def get_init_consts() -> InitCosts:
    """
    Returns an instance of InitCosts containing initialization constants.

    :return: An InitCosts instance with predefined initial data.
    """

    return InitCosts()
