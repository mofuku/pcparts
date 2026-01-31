"""
Example scraper implementation.

This is a template showing how to implement a retailer scraper.
Copy and modify for actual retailers.
"""

from decimal import Decimal
from typing import AsyncIterator

from app.scrapers.base import BaseScraper, ScrapedPrice


class ExampleScraper(BaseScraper):
    """
    Example scraper template.
    
    To implement a real scraper:
    1. Copy this file to <retailer>.py
    2. Update retailer info
    3. Implement scrape_category() with actual scraping logic
    """

    retailer_slug = "example-us"
    retailer_name = "Example Store"
    base_url = "https://example.com"
    country_code = "US"
    currency = "USD"

    # Category URL mappings
    CATEGORY_URLS = {
        "cpu": "/category/processors",
        "gpu": "/category/graphics-cards",
        "ram": "/category/memory",
        "motherboard": "/category/motherboards",
        "storage": "/category/storage",
        "psu": "/category/power-supplies",
        "case": "/category/cases",
        "cooler": "/category/cooling",
    }

    async def scrape_category(self, category_slug: str) -> AsyncIterator[ScrapedPrice]:
        """
        Scrape all products in a category.
        
        Real implementation would:
        1. Fetch category listing page
        2. Parse products (with pagination)
        3. Yield ScrapedPrice for each
        """
        if category_slug not in self.CATEGORY_URLS:
            self.logger.warning(f"Unknown category: {category_slug}")
            return

        url = f"{self.base_url}{self.CATEGORY_URLS[category_slug]}"
        self.logger.info(f"Scraping {url}")

        # Example: Fetch and parse
        # response = await self.client.get(url)
        # soup = BeautifulSoup(response.text, "lxml")
        # for product in soup.select(".product-card"):
        #     yield ScrapedPrice(...)

        # Placeholder - in real implementation, parse actual HTML
        yield ScrapedPrice(
            manufacturer="Example",
            model="Test Product",
            price=Decimal("299.99"),
            currency="USD",
            in_stock=True,
            product_url=f"{self.base_url}/product/123",
        )

    async def scrape_product(self, product_url: str) -> ScrapedPrice | None:
        """Scrape a single product page for price updates."""
        response = await self.client.get(product_url)

        if response.status_code != 200:
            return None

        # Parse product page
        # soup = BeautifulSoup(response.text, "lxml")
        # price = soup.select_one(".price").text
        # ...

        return None  # Implement actual parsing
