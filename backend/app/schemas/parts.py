"""Part schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PartSpecSchema(BaseModel):
    """Part specification key-value pair."""

    key: str
    value: str
    unit: str | None = None


class CategoryCreate(BaseModel):
    """Create a new category."""

    slug: str
    name: str
    icon: str | None = None


class CategoryResponse(BaseModel):
    """Category response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    icon: str | None


class PartCreate(BaseModel):
    """Create a new part."""

    manufacturer: str
    model: str
    full_name: str
    category_id: int
    image_url: str | None = None
    description: str | None = None
    specs: list[PartSpecSchema] = []


class PartResponse(BaseModel):
    """Part response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    manufacturer: str
    model: str
    full_name: str
    category_id: int
    image_url: str | None
    description: str | None
    created_at: datetime
    specs: list[PartSpecSchema] = []


class PartPriceInfo(BaseModel):
    """Price info for a part (latest from each retailer)."""

    retailer_slug: str
    retailer_name: str
    price: Decimal
    currency: str
    in_stock: bool
    product_url: str
    scraped_at: datetime


class PartWithPrices(PartResponse):
    """Part with latest prices from all retailers."""

    prices: list[PartPriceInfo] = []
    lowest_price: Decimal | None = None
    category: CategoryResponse | None = None
