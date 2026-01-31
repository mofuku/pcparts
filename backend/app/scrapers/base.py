"""Base scraper interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import AsyncIterator
import logging

import httpx


@dataclass
class ScrapedPrice:
    """A scraped price result."""

    # Product identification (used to match to our parts)
    manufacturer: str
    model: str  # or product_name
    sku: str | None = None  # retailer SKU

    # Price data
    price: Decimal
    currency: str
    in_stock: bool = True
    stock_count: int | None = None

    # URLs
    product_url: str
    image_url: str | None = None

    # Metadata
    scraped_at: datetime | None = None

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow()


class BaseScraper(ABC):
    """
    Base class for retailer scrapers.
    
    Each retailer scraper should:
    1. Inherit from this class
    2. Implement `scrape_category()` to yield prices
    3. Optionally override `setup()` and `teardown()` for browser etc.
    
    Example:
        class AmazonScraper(BaseScraper):
            retailer_slug = "amazon-us"
            
            async def scrape_category(self, category_slug: str):
                # ... scraping logic ...
                yield ScrapedPrice(...)
    """

    # Override in subclass
    retailer_slug: str = ""
    retailer_name: str = ""
    base_url: str = ""
    country_code: str = "US"
    currency: str = "USD"

    # Rate limiting
    request_delay_seconds: float = 1.0
    max_retries: int = 3

    def __init__(self):
        self.logger = logging.getLogger(f"scraper.{self.retailer_slug}")
        self._client: httpx.AsyncClient | None = None

    async def setup(self):
        """Initialize resources (HTTP client, browser, etc.)."""
        self._client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; PCParts/1.0)",
            },
        )

    async def teardown(self):
        """Clean up resources."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client."""
        if not self._client:
            raise RuntimeError("Scraper not initialized. Call setup() first.")
        return self._client

    @abstractmethod
    async def scrape_category(self, category_slug: str) -> AsyncIterator[ScrapedPrice]:
        """
        Scrape all products in a category.
        
        Args:
            category_slug: Category to scrape ("cpu", "gpu", etc.)
            
        Yields:
            ScrapedPrice objects for each product found.
        """
        pass

    async def scrape_product(self, product_url: str) -> ScrapedPrice | None:
        """
        Scrape a single product page.
        
        Optional - implement for targeted updates.
        """
        raise NotImplementedError

    async def search(self, query: str) -> AsyncIterator[ScrapedPrice]:
        """
        Search for products.
        
        Optional - implement for product discovery.
        """
        raise NotImplementedError

    async def __aenter__(self):
        await self.setup()
        return self

    async def __aexit__(self, *args):
        await self.teardown()
