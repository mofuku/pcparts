"""Price and retailer schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class RetailerCreate(BaseModel):
    """Create a new retailer."""

    slug: str
    name: str
    base_url: str
    country_code: str
    currency: str


class RetailerResponse(BaseModel):
    """Retailer response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    base_url: str
    country_code: str
    currency: str
    is_active: bool
    last_scraped_at: datetime | None


class PriceCreate(BaseModel):
    """Create a price record (from scraper)."""

    part_id: int
    retailer_id: int
    price: Decimal
    currency: str
    in_stock: bool = True
    stock_count: int | None = None
    product_url: str


class PriceResponse(BaseModel):
    """Price response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    part_id: int
    retailer_id: int
    price: Decimal
    currency: str
    in_stock: bool
    stock_count: int | None
    product_url: str
    scraped_at: datetime


class PricePoint(BaseModel):
    """Single point in price history."""

    price: Decimal
    in_stock: bool
    scraped_at: datetime


class PriceHistory(BaseModel):
    """Price history for a part at a retailer."""

    part_id: int
    retailer_id: int
    retailer_name: str
    currency: str
    history: list[PricePoint]
    lowest_price: Decimal
    highest_price: Decimal
    current_price: Decimal | None
