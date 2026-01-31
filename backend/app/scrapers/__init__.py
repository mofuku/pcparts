"""
Scraper framework for PCParts.

Each retailer has its own scraper module that implements the BaseScraper interface.
Scrapers are registered and run via the ScraperManager.

Architecture:
    - BaseScraper: Abstract base class with common functionality
    - ScraperManager: Orchestrates scraping across retailers
    - Individual scrapers: One per retailer (amazon.py, newegg.py, etc.)

The scrapers are designed to be:
    - Async-first for concurrent operation
    - Rate-limited to respect retailer ToS
    - Resumable (track last scraped product)
    - Observable (logging, metrics)
"""

from app.scrapers.base import BaseScraper, ScrapedPrice
from app.scrapers.manager import ScraperManager

__all__ = ["BaseScraper", "ScrapedPrice", "ScraperManager"]
