"""Application configuration."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    # App
    app_name: str = "PCParts API"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./pcparts.db"

    # Scraping
    scrape_interval_minutes: int = 60
    max_concurrent_scrapers: int = 5
    request_timeout_seconds: int = 30

    # Price alerts
    price_drop_threshold_percent: float = 5.0

    class Config:
        env_file = ".env"
        env_prefix = "PCPARTS_"


@lru_cache
def get_settings() -> Settings:
    return Settings()
