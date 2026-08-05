from typing import Any, List, Optional

from pydantic import AnyHttpUrl, PostgresDsn, field_validator, model_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_SECRET = "CHANGE_THIS_IN_PRODUCTION"


class Settings(BaseSettings):
    """
    Centralized configuration management.
    Loads from environment variables or a .env file.
    """
    PROJECT_NAME: str = "PHOENIX API"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API Settings
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "phoenix"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./phoenix.db"

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str) and v.startswith("postgres"):
            return v
        values = info.data
        server = values.get("POSTGRES_SERVER")
        if server and server != "localhost":
            # Pydantic v2: parameter is `username`, not `user`
            return str(PostgresDsn.build(
                scheme="postgresql",
                username=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=server,
                path=values.get("POSTGRES_DB") or "",
            ))
        return "sqlite:///./phoenix_test.db"

    # Security
    SECRET_KEY: str = _DEFAULT_SECRET
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @model_validator(mode="after")
    def _guard_secret_key(self) -> "Settings":
        """
        Prevent startup with the default insecure SECRET_KEY in non-development environments.
        This is a hard fail — if you see this error, set SECRET_KEY in your .env file.
        """
        if self.ENVIRONMENT != "development" and self.SECRET_KEY == _DEFAULT_SECRET:
            raise ValueError(
                "CRITICAL: SECRET_KEY must be changed from the default value in non-development environments. "
                "Set a strong random SECRET_KEY in your .env file before deploying."
            )
        return self

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

