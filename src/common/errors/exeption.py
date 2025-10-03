from enum import Enum

from fastapi import HTTPException


class BackendException(HTTPException):
    """
    Custom HTTP exception for backend errors with extended error information.

    Extends FastAPI's HTTPException to include:
    - Error code from provided Enum
    - HTTP status code
    - Human-readable description
    - Optional root cause information

    :param error: Enum instance containing error details in format
            (code, status, description)
    :param cause: Optional string with technical details about the error cause
    """

    cause: str = ""

    def __init__(
        self,
        error: Enum,
        *,
        cause: str = "",
    ):
        """
        Initialize the backend exception with error details.

        :param error: Enum containing error details in format
                (code: str, status: int, description: str)
        :param cause: Optional technical details about the root cause of the error,
                defaults to empty string
        """

        if not isinstance(error, Enum):
            msg = "The provided error must be an instance of Enum"
            raise TypeError(msg)

        self.error_code = error.value[0]
        self.status_code = error.value[1]
        self.description = error.value[2]
        self.cause = cause
