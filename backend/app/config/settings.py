from functools import lru_cache

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="development", alias="APP_ENV")
    app_name: str = Field(default="InvElRey", alias="APP_NAME")
    api_v1_prefix: str = "/api/v1"

    database_url: PostgresDsn = Field(alias="DATABASE_URL")

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_hours: int = Field(default=8, alias="ACCESS_TOKEN_EXPIRE_HOURS")

    cloudinary_cloud_name: str = Field(alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(alias="CLOUDINARY_API_SECRET")

    frontend_url: str = Field(default="http://localhost:5173", alias="FRONTEND_URL")

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret_key(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT_SECRET_KEY must contain at least 32 characters.")
        return value

    @property
    def sqlalchemy_database_url(self) -> str:
        return str(self.database_url)

    @property
    def cors_origins(self) -> list[str]:
        return [self.frontend_url]


@lru_cache
def get_settings() -> Settings:
    return Settings()
