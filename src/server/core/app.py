import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi_pagination import add_pagination
from starlette.middleware.sessions import SessionMiddleware

from src.common.errors import BackendException
from src.config.docs.deps import get_app_description, get_tags_metadata
from src.config.settings.deps import get_settings

# from src.server.core.controllers import api_controller
from src.server.middleware.deps import (
    get_exception_handler,
    get_exception_middleware,
    get_postgres_context_session_middleware,
    get_validation_exception_handler,
)

# === Constants === #
origins = [
    "*",
]


# === FastAPI App unique id === #
def custom_generate_unique_id(route: APIRoute) -> str:
    return route.name


# === FastAPI App Initialization === #
app = FastAPI(
    debug=True,
    title=get_settings().project.PROJECT_NAME,
    version=get_settings().project.PROJECT_VERSION,
    openapi_url=f"{get_settings().project.API_V1_STR}/openapi.json",
    openapi_tags=get_tags_metadata().get_tags_metadata(),
    exception_handlers={BackendException: get_exception_handler().handle},
    description=get_app_description().build_description(),
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none",
    },
    generate_unique_id_function=custom_generate_unique_id,
)


# === Middleware Setup === #
def setup_middleware():
    """
    Configures middleware for CORS and session handling.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=get_settings().project.OAUTH_SECRET_KEY,
    )
    app.middleware("http")(get_exception_middleware())
    app.middleware("http")(get_postgres_context_session_middleware())

    app.exception_handler(RequestValidationError)(
        get_validation_exception_handler().handle,
    )


# === Router Setup === #
def include_routers():
    """
    Includes all application routes with API versioning.
    """
    # app.include_router(api_controller, prefix=get_settings().project.API_V1_STR)


# === Pagination Setup === #
def setup_pagination():
    """
    Sets up pagination for FastAPI endpoints.
    """
    add_pagination(app)


def set_gunicorn_logs() -> None:
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger = logging.getLogger("gunicorn")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.setLevel(gunicorn_logger.level)


# === Initialize App Configuration === #
def initialize_app():
    """
    Calls all setup functions to configure the application.
    """
    setup_middleware()
    include_routers()
    setup_pagination()

    if get_settings().project.IS_PROD_MODE:
        set_gunicorn_logs()


# === Run App Initialization === #
initialize_app()
