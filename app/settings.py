import os
from datetime import timedelta
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DEBUG: bool = bool(os.environ.get("DEBUG", True))
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", "sqlite:///app.db").replace("postgres://",
                                                                                              "postgresql://")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY: str = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SESSION_COOKIE = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_SUPPORTS_CREDENTIALS = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
