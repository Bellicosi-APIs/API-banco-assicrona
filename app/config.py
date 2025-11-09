from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # JWT Configuration
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "sqlite+aiosqlite:///./bank.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

