import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.adapters.repositories.postgres import PostgresBaseRepo
from src.common.constants import ErrorCodesEnums
from src.common.decorators import LoggingFunctionInfo
from src.common.errors import BackendException
from src.modules.activity.interfaces import IActivityPsqlRepo
from src.modules.activity.models import ActivityModel
from src.modules.activity.schemas import ActivityCreate, ActivityUpdate


class ActivityPsqlRepo(
    PostgresBaseRepo[ActivityModel, ActivityCreate, ActivityUpdate],
    IActivityPsqlRepo,
):
    """Repository implementation for Activity entities using PostgreSQL."""

    def __init__(
        self,
        db: AsyncSession,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initializes the repository with database session, error codes, and logger.

        :param db: AsyncSession instance for database connectivity.
        :param errors: Enumeration of error codes for handling repository errors.
        :param logger: Logger instance for logging repository operations.
        """

        super().__init__(db=db, model=ActivityModel, errors=errors, logger=logger)
        self._errors = errors
        self._logger = logger

    async def _get_depth(self, sid: UUID) -> int:
        """
        Calculate the depth of an activity in the hierarchy based on parent
        relationships.

        :param sid: UUID of the activity.
        :return: Integer representing the depth (number of ancestors).
        """

        depth = 0
        current_sid = sid
        while current_sid:
            activity = await super().get(sid=current_sid)
            if not activity or activity.parent_sid is None:
                break
            current_sid = activity.parent_sid
            depth += 1

        self._logger.debug("Computed depth %d for activity %s", depth, sid)

        return depth

    @LoggingFunctionInfo(description="Retrieves an activity by its name.")
    async def get_by_name(
        self, name: str, custom_options: tuple[ExecutableOption, ...] | None = None
    ) -> ActivityModel:
        """
        Fetches a single activity matching the specified name.

        :param name: The name of the activity.
        :param custom_options: Optional SQLAlchemy execution options, such as query hints.
        :return: ActivityModel instance with the specified name.
        """

        query = await self._apply_options(
            query=select(self._model).where(self._model.name == name),
            options=custom_options,
        )

        self._logger.debug("Retrieved activity by name: %s", name)
        return await self._get_single_result(query)

    @LoggingFunctionInfo(
        description="Creates a new activity ensuring hierarchical depth limits."
    )
    async def create(
        self, *, obj_in: ActivityCreate, with_commit: bool = True
    ) -> ActivityModel:
        """
        Creates a new activity, validating that the parent depth does not exceed the
        max allowed (3).

        :param obj_in: ActivityCreate instance containing new activity data.
        :param with_commit: Whether to commit the transaction immediately.
        :return: Created ActivityModel instance.
        """

        if obj_in.parent_sid:
            depth = await self._get_depth(obj_in.parent_sid)
            if depth >= 3:  # noqa: PLR2004
                self._logger.warning(
                    "Attempted to create activity exceeding max depth at parent %s with depth %d",
                    obj_in.parent_sid,
                    depth,
                )

                raise BackendException(error=self._errors.Activity.EXCEED_MAX_DEPTH)

        self._logger.info("Creating new activity with data: %s", obj_in)

        return await super().create(obj_in=obj_in, with_commit=with_commit)
