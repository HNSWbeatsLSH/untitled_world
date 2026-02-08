"""
Core configuration for the Data Investigation Platform.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Data Investigation Platform"
    VERSION: str = "0.1.0"

    # Database - defaults to SQLite for easy testing
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./investigation_platform.db")

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
