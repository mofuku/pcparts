"""Scraper orchestration."""

import asyncio
import logging
from datetime import datetime
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.scrapers.base import BaseScraper, ScrapedPrice
from app.models import Retailer, Part, Price, Category
from app.config import get_settings

logger = logging.getLogger("scraper.manager")
settings = get_settings()


class ScraperManager:
    """
    Manages and orchestrates scrapers.
    
    Responsibilities:
    - Register scrapers for each retailer
    - Run scrapers concurrently (with limits)
    - Match scraped products to our parts database
    - Record prices
    - Handle errors and retries
    
    Usage:
        manager = ScraperManager(db_session)
        manager.register(AmazonScraper())
        manager.register(NeweggScraper())
        
        await manager.run_all(categories=["cpu", "gpu"])
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.scrapers: dict[str, BaseScraper] = {}
        self._semaphore = asyncio.Semaphore(settings.max_concurrent_scrapers)

    def register(self, scraper: BaseScraper):
        """Register a scraper."""
        self.scrapers[scraper.retailer_slug] = scraper
        logger.info(f"Registered scraper: {scraper.retailer_slug}")

    async def run_all(self, categories: list[str] | None = None):
        """
        Run all registered scrapers.
        
        Args:
            categories: Categories to scrape. If None, scrapes all.
        """
        if not categories:
            # Get all category slugs from DB
            from sqlalchemy import select

            result = await self.db.execute(select(Category.slug))
            categories = [row[0] for row in result.all()]

        if not categories:
            logger.warning("No categories to scrape")
            return

        tasks = []
        for slug, scraper in self.scrapers.items():
            for category in categories:
                tasks.append(self._run_scraper(scraper, category))

        await asyncio.gather(*tasks, return_exceptions=True)

    async def _run_scraper(self, scraper: BaseScraper, category: str):
        """Run a single scraper for a category."""
        async with self._semaphore:
            try:
                async with scraper:
                    logger.info(f"Starting {scraper.retailer_slug} for {category}")
                    count = 0

                    async for scraped in scraper.scrape_category(category):
                        await self._process_scraped_price(scraper, scraped)
                        count += 1

                    logger.info(f"Completed {scraper.retailer_slug}/{category}: {count} prices")

                    # Update retailer last_scraped_at
                    await self._update_retailer_status(scraper.retailer_slug, None)

            except Exception as e:
                logger.error(f"Scraper {scraper.retailer_slug} failed: {e}")
                await self._update_retailer_status(scraper.retailer_slug, str(e))

    async def _process_scraped_price(self, scraper: BaseScraper, scraped: ScrapedPrice):
        """Match scraped price to part and record it."""
        # Try to find matching part
        from sqlalchemy import select

        # Simple matching by manufacturer + model
        # TODO: Fuzzy matching, ML-based matching
        result = await self.db.execute(
            select(Part).where(
                Part.manufacturer.ilike(f"%{scraped.manufacturer}%"),
                Part.model.ilike(f"%{scraped.model}%"),
            )
        )
        part = result.scalar_one_or_none()

        if not part:
            # TODO: Queue for manual review / auto-create?
            logger.debug(f"No match for {scraped.manufacturer} {scraped.model}")
            return

        # Get retailer
        result = await self.db.execute(
            select(Retailer).where(Retailer.slug == scraper.retailer_slug)
        )
        retailer = result.scalar_one_or_none()

        if not retailer:
            logger.error(f"Retailer not found: {scraper.retailer_slug}")
            return

        # Record price
        price = Price(
            part_id=part.id,
            retailer_id=retailer.id,
            price=scraped.price,
            currency=scraped.currency,
            in_stock=scraped.in_stock,
            stock_count=scraped.stock_count,
            product_url=scraped.product_url,
        )
        self.db.add(price)
        await self.db.commit()

    async def _update_retailer_status(self, slug: str, error: str | None):
        """Update retailer scraping status."""
        from sqlalchemy import select, update

        await self.db.execute(
            update(Retailer)
            .where(Retailer.slug == slug)
            .values(last_scraped_at=datetime.utcnow(), scrape_error=error)
        )
        await self.db.commit()
