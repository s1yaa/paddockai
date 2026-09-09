"""
PaddockAI — Application Configuration
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://paddockai:paddockai_dev@localhost:5432/paddockai"
    database_url_sync: str = "postgresql://paddockai:paddockai_dev@localhost:5432/paddockai"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Demo
    demo_mode: bool = True

    # OpenF1
    openf1_base_url: str = "https://api.openf1.org/v1"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
