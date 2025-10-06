import asyncio
import logging
import sys

from sqlalchemy.sql import text
from tenacity import (
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    wait_fixed,
)

sys.path = ["", ".."] + sys.path[1:]

from src.client.storages.deps import get_postgres_session_provider  # noqa: E402, I001, RUF100
from src.client.storages.postgres.core import PostgresSessionContextManager  # noqa: E402, I001, RUF100

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(60 * 5),
    wait=wait_fixed(1),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARNING),
)
async def init() -> None:
    PostgresSessionContextManager.set_session_context(1)

    session_provider = get_postgres_session_provider()

    db = session_provider.get_session()

    try:
        response = await db.execute(text("SELECT 1"))
        logger.info("Response value: %s", response.first())
    except Exception as e:
        logger.error(e)  # noqa: TRY400
        raise e  # noqa: TRY201
    finally:
        await db.close()


async def main() -> None:
    logger.info("Ping PostgreSQL")
    await init()
    logger.info("PostgreSQL pong'd")


if __name__ == "__main__":
    asyncio.run(main())
