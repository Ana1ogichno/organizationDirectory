from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    # API
    API_V1_STR: str = "/api/v1"

    # Service Info
    PROJECT_VERSION: str = "0.0.1"  # Изменять вручную
    PROJECT_NAME: str = "StripesID Iam Service"

    HOST: str = Field("localhost")
    PORT: int = Field(8000)
    MODE: str = Field(..., alias="SERVER_MODE")
    LOG_LEVEL: str = Field(..., alias="LOG_LEVEL")
    IS_LOCAL_MODE: bool = False
    IS_TEST_MODE: bool = False
    IS_PROD_MODE: bool = False

    @field_validator("IS_LOCAL_MODE", mode="before")
    def assemble_local_mode(cls, _: bool, values: ValidationInfo) -> bool:  # noqa: N805
        return values.data.get("MODE") == "local"

    @field_validator("IS_TEST_MODE", mode="before")
    def assemble_test_mode(cls, _: bool, values: ValidationInfo) -> bool:  # noqa: N805
        return values.data.get("MODE") == "test"

    @field_validator("IS_PROD_MODE", mode="before")
    def assemble_prod_mode(cls, _: bool, values: ValidationInfo) -> bool:  # noqa: N805
        return values.data.get("MODE") == "prod"

    OAUTH_SECRET_KEY: str = Field("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")

    TZ: str = Field("Europe/Moscow")

    ON_PRODUCTION: bool = Field(False)
