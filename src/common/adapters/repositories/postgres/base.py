import logging
from collections.abc import Sequence
from typing import Any, TypeVar
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Result, Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.common.constants import ErrorCodesEnums
from src.common.decorators.logger import LoggingFunctionInfo
from src.common.interfaces import IPostgresBaseRepo
from src.common.models import CoreModel
from src.common.schemas import Pagination
from src.server.middleware.exception import BackendException

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class PostgresBaseRepo(
    IPostgresBaseRepo[ModelType, CreateSchemaType, UpdateSchemaType]
):
    """
    Generic asynchronous CRUD repository for SQLAlchemy models.

    Provides base methods for retrieving, creating, updating, and deleting records.
    Designed for reuse and consistency across multiple domain entities.
    """

    def __init__(
        self,
        db: AsyncSession,
        model: type[ModelType],
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initialize the CRUD repository with model, database session, error handler,
        and logger.

        :param db: SQLAlchemy asynchronous session for database operations.
        :param model: SQLAlchemy ORM model class to operate on.
        :param errors: Error enumerations to raise domain-specific exceptions.
        :param logger: Logger instance used for logging internal actions.
        """

        self._db = db
        self._model = model
        self._errors = errors
        self._logger = logger

    @staticmethod
    async def _apply_options(
        query: Select, options: tuple[ExecutableOption, ...] | None
    ) -> Select:
        """
        Apply SQLAlchemy query options if any.

        :param query: SQLAlchemy Select query.
        :param options: Tuple of ExecutableOptions to apply.
        :return: Query with applied options.
        """

        if options:
            query = query.options(*options)
        return query

    async def _get_single_result(self, query: Select) -> ModelType | None:
        """
        Execute the query and return a single result.

        :param query: SQLAlchemy Select query.
        :return: Single result or None.
        """

        result: Result = await self._db.execute(query)
        return result.scalars().first()

    async def _get_all_results(self, query: Select) -> Sequence[ModelType | Any]:
        """
        Execute the query and return all results.

        :param query: SQLAlchemy Select query.
        :return: Sequence of results.
        """

        result: Result = await self._db.execute(query)
        return result.scalars().all()

    async def _commit_and_refresh(self, db_obj: ModelType, with_commit: bool) -> None:
        """
        Helper method to commit and refresh the database object.

        :param db_obj: The database object to commit and refresh.
        :param with_commit: Whether to commit the transaction (True) or just flush
                (False).
        """

        if with_commit:
            await self._db.commit()
            await self._db.refresh(db_obj)
            self._logger.debug("%s created and committed", self._model.__name__)
        else:
            await self._db.flush()
            self._logger.debug("%s created and flushed", self._model.__name__)

    async def _apply_pagination(
        self,
        query: Select,
        pagination_params: Pagination,
    ) -> (Sequence[ModelType], int):
        """
        Applies pagination to the provided query, returning paginated results and the
        total count.

        :param query: SQLAlchemy Select query to paginate.
        :param pagination_params: Pagination parameters containing limit and offset.
        :return: A tuple with a sequence of model instances and the total number of
                matched rows.
        """

        count_query = select(func.count()).select_from(query.subquery())
        total = await self._get_single_result(query=count_query)

        paginated_query = query.limit(pagination_params.limit).offset(
            pagination_params.offset
        )
        items = await self._get_all_results(query=paginated_query)

        return items, total

    @LoggingFunctionInfo(
        description="Fetch a single record by its SID from the database"
    )
    async def get(
        self, sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ModelType | None:
        """
        Retrieve a single object by its SID.

        :param sid: Unique identifier of the model.
        :param custom_options: Optional SQLAlchemy query options.
        :return: Found model or None.
        """

        query = await self._apply_options(
            query=select(self._model).where(self._model.sid == sid),
            options=custom_options,
        )

        self._logger.debug("Fetching %s by SID: %s", self._model.__name__, sid)
        return await self._get_single_result(query)

    @LoggingFunctionInfo(
        description="Retrieve all records of the model from the database"
    )
    async def get_all(
        self, custom_options: tuple[ExecutableOption, ...] = None
    ) -> Sequence[ModelType]:
        """
        Retrieve all records for the model.

        :param custom_options: Optional SQLAlchemy query options.
        :return: List of all model instances.
        """

        query = await self._apply_options(
            query=select(self._model), options=custom_options
        )

        self._logger.debug("Fetching all %s records", self._model.__name__)
        return await self._get_all_results(query)

    @LoggingFunctionInfo(description="Create a new record in the database")
    async def create(
        self, *, obj_in: CreateSchemaType, with_commit: bool = True
    ) -> ModelType:
        """
        Create a new record in the database.

        :param obj_in: Input data for creation.
        :param with_commit: Whether to commit the transaction immediately.
        :return: Created model instance.
        """

        try:
            db_obj = self._model(**obj_in.model_dump())
            self._db.add(db_obj)

            await self._commit_and_refresh(db_obj, with_commit)

        except IntegrityError as e:
            self._logger.debug(
                "Failed to create %s due to IntegrityError. Error: %s",
                self._model.__name__,
                e,
            )
            raise BackendException(error=self._errors.Common.NOT_UNIQUE) from e

        else:
            return db_obj

    @LoggingFunctionInfo(description="Update an existing record in the database")
    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        with_commit: bool = True,
    ) -> ModelType:
        """
        Update an existing record in the database.

        :param db_obj: The current database model instance.
        :param obj_in: Input data as dict or UpdateSchemaType.
        :param with_commit: Whether to commit the transaction.
        :return: Updated model instance.
        """

        try:
            update_data = (
                obj_in
                if isinstance(obj_in, dict)
                else obj_in.model_dump(exclude_unset=True, exclude_none=True)
            )

            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            self._db.add(db_obj)

            if with_commit:
                await self._db.commit()
                await self._db.refresh(db_obj)
                self._logger.debug(
                    "%s with SID=%s updated and committed",
                    self._model.__name__,
                    getattr(db_obj, "sid", "?"),
                )
            else:
                await self._db.flush()
                self._logger.debug(
                    "%s with SID=%s updated and flushed",
                    self._model.__name__,
                    getattr(db_obj, "sid", "?"),
                )

        except IntegrityError as e:
            self._logger.debug(
                "Failed to update %s due to IntegrityError", self._model.__name__
            )
            raise BackendException(error=self._errors.Common.NOT_UNIQUE) from e
        else:
            return db_obj

    @LoggingFunctionInfo(description="Delete a record from the database by its SID")
    async def delete(self, *, sid: UUID, with_commit: bool = True) -> ModelType | None:
        """
        Delete a record by its SID.

        :param sid: Unique identifier of the model to delete.
        :param with_commit: Whether to commit the transaction immediately.
        :return: Deleted model instance or None if not found.
        """

        obj = await self.get(sid)
        if obj is None:
            self._logger.debug(
                "%s with SID={sid} not found for deletion", self._model.__name__
            )
            return None

        await self._db.delete(obj)

        if with_commit:
            await self._db.commit()
            self._logger.debug(
                "%s with SID={sid} deleted and committed", self._model.__name__
            )
        else:
            await self._db.flush()
            self._logger.debug(
                "%s with SID={sid} deleted and flushed", self._model.__name__
            )

        return obj
