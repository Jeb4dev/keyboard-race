import os
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DEBUG: bool = bool(os.environ.get("DEBUG", True))
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "super-secret-key")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
