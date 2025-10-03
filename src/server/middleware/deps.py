from src.client.storages.deps import get_postgres_session_provider
from src.client.storages.postgres.core.deps import get_postgres_session_context_manager
from src.common.constants.deps import get_error_codes
from src.common.logger.constants.deps import get_logger_config
from src.common.logger.deps import get_base_logger, get_logger_manager
from src.server.interfaces import (
    IExceptionHandler,
    IExceptionMiddleware,
    IPostgresContextSessionMiddleware,
    IValidationExceptionHandler,
)
from src.server.middleware.exception import (
    BackendExceptionHandler,
    ExceptionMiddleware,
    ValidationExceptionHandler,
)
from src.server.middleware.psql_context_manager import PostgresContextSessionMiddleware


def get_exception_handler() -> IExceptionHandler:
    """
    Returns an instance of BackendExceptionHandler.

    This function provides the exception handler to be used by FastAPI.
    It is responsible for handling `BackendException` errors by returning
    a structured JSON response with error details.

    :return: An instance of `BackendExceptionHandler`, which handles BackendException
            errors.
    """
    return BackendExceptionHandler()


def get_exception_middleware() -> IExceptionMiddleware:
    """
    Returns an instance of ExceptionMiddleware.

    This function provides the middleware that handles any uncaught exceptions
    during the request-response cycle. It logs the exception and returns a default
    error response when an unhandled error occurs.

    :return: An instance of `ExceptionMiddleware`, which handles uncaught exceptions in
            FastAPI.
    """

    return ExceptionMiddleware(
        logger=get_base_logger(get_logger_manager(get_logger_config())),
        errors=get_error_codes(),
    )


def get_validation_exception_handler() -> IValidationExceptionHandler:
    """
    Returns an instance of ValidationExceptionHandler.

    This function provides the exception handler specifically for validation errors.
    It catches validation errors raised during request parsing and returns a structured
    JSON response with the error details.

    :return: An instance of `ValidationExceptionHandler`, which handles validation
            errors in FastAPI.
    """

    return ValidationExceptionHandler(
        logger=get_base_logger(get_logger_manager(get_logger_config())),
        errors=get_error_codes(),
    )


def get_postgres_context_session_middleware() -> IPostgresContextSessionMiddleware:
    """
    Returns an instance of ValidationExceptionHandler.

    This function provides the exception handler specifically for validation errors.
    It catches validation errors raised during request parsing and returns a structured
    JSON response with the error details.

    :return: An instance of `ValidationExceptionHandler`, which handles validation
            errors in FastAPI.
    """

    return PostgresContextSessionMiddleware(
        errors=get_error_codes(),
        postgres_session_provider=get_postgres_session_provider(),
        postgres_session_context_manager=get_postgres_session_context_manager(),
    )
