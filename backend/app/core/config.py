from typing import Any, List, Optional

from pydantic import AnyHttpUrl, PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


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
        if values.get("POSTGRES_SERVER") and values.get("POSTGRES_SERVER") != "localhost":
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_SERVER"),
                path=f"/{values.get('POSTGRES_DB') or ''}",
            )
        return "sqlite:///./phoenix_test.db"

    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
