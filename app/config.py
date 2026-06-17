from pydantic_settings import BaseSettings
from pydantic import ConfigDict, computed_field, PostgresDsn
from functools import lru_cache

DB_SCHEME = "postgresql+asyncpg"

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    CRAWL_LIMIT: int = 20
    CRAWL_TIMEOUT: int = 10
    USER_AGENT: str = "aeo-audit-bot/1.0"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "aeo_audit"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        dsn = PostgresDsn.build(
            scheme=DB_SCHEME,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
            username=self.DB_USER,
            password=self.DB_PASSWORD
        )
        return str(dsn)


@lru_cache
def get_settings() -> Settings:
    return Settings()