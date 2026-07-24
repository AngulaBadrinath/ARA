from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = Field(
        default="postgresql+psycopg://postgres:Badri%40123@localhost:5432/ara_db",
        alias="DATABASE_URL",
    )

    redis_url: str = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL",
    )

    secret_key: str = Field(
        default="change-me",
        alias="SECRET_KEY",
    )

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    cors_origins: str = Field(
        default="http://localhost:3000",
        alias="CORS_ORIGINS",
    )

    s3_endpoint: str = Field(
        default="http://localhost:9000",
        alias="S3_ENDPOINT",
    )

    s3_access_key: str = Field(
        default="ara_minio",
        alias="S3_ACCESS_KEY",
    )

    s3_secret_key: str = Field(
        default="ara_minio_secret",
        alias="S3_SECRET_KEY",
    )

    s3_bucket: str = Field(
        default="resumes",
        alias="S3_BUCKET",
    )

    s3_region: str = Field(
        default="us-east-1",
        alias="S3_REGION",
    )

    s3_use_ssl: bool = Field(
        default=False,
        alias="S3_USE_SSL",
    )

    llm_provider: str = Field(
        default="ollama",
        alias="LLM_PROVIDER",
    )

    llm_api_base: str = Field(
        default="http://localhost:11434",
        alias="LLM_API_BASE",
    )

    llm_model: str = Field(
        default="qwen2.5-coder:7b",
        alias="LLM_MODEL",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()