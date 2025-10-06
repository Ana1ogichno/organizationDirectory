from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, APIKeyHeader

from src.common.constants import ErrorCodesEnums
from src.common.constants.deps import get_error_codes
from src.common.errors import BackendException
from src.config.settings.deps import get_settings

APIKey = Annotated[
    str,
    Depends(
        APIKeyHeader(
            name="X-APIKey-Auth",
            scheme_name="AuthSchema",
            description="API token",
            auto_error=False,
        )
    ),
]


async def get_api_key(
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    api_key: APIKey,
) -> str:
    if not api_key:
        raise BackendException(error_codes.Common.API_KEY_NOT_FOUND)
    if api_key != get_settings().project.SECRET_API_KEY:
        raise BackendException(error_codes.Common.INVALID_API_KEY)
    return api_key
