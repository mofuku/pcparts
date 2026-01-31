"""Price and retailer models."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.parts import Part


class Retailer(Base):
    """
    A retailer/store we scrape prices from.
    
    Examples: Amazon, Newegg, B&H Photo, Micro Center
    """

    __tablename__ = "retailers"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # "amazon-us"
    name: Mapped[str] = mapped_column(String(100))  # "Amazon US"
    
    # Scraping config
    base_url: Mapped[str] = mapped_column(String(200))
    country_code: Mapped[str] = mapped_column(String(2), index=True)  # "US", "UK", "DE"
    currency: Mapped[str] = mapped_column(String(3))  # "USD", "EUR", "GBP"
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    last_scraped_at: Mapped[Optional[datetime]] = mapped_column()
    scrape_error: Mapped[Optional[str]] = mapped_column(Text)  # last error if any

    # Relationships
    prices: Mapped[list["Price"]] = relationship(back_populates="retailer")

    def __repr__(self) -> str:
        return f"<Retailer {self.slug}>"


class Price(Base):
    """
    A price snapshot for a part at a specific retailer.
    
    New rows are inserted for price history tracking.
    Query latest prices with: SELECT ... ORDER BY scraped_at DESC LIMIT 1
    """

    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts.id"), index=True)
    retailer_id: Mapped[int] = mapped_column(ForeignKey("retailers.id"), index=True)
    
    # Price data
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3))  # inherited from retailer usually
    
    # Stock status
    in_stock: Mapped[bool] = mapped_column(default=True)
    stock_count: Mapped[Optional[int]] = mapped_column()  # if available
    
    # Links
    product_url: Mapped[str] = mapped_column(Text)
    
    # Metadata
    scraped_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)

    # Relationships
    part: Mapped["Part"] = relationship(back_populates="prices")
    retailer: Mapped["Retailer"] = relationship(back_populates="prices")

    # Index for efficient "latest price per part/retailer" queries
    __table_args__ = (
        UniqueConstraint("part_id", "retailer_id", "scraped_at", name="uq_price_snapshot"),
    )

    def __repr__(self) -> str:
        return f"<Price {self.part_id}@{self.retailer_id}: {self.price}>"


class PriceAlert(Base):
    """
    User price alerts - notify when price drops below target.
    
    Future: link to user_id when auth is added.
    """

    __tablename__ = "price_alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts.id"), index=True)
    
    # Alert config
    target_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    email: Mapped[Optional[str]] = mapped_column(String(200))  # simple MVP, replace with user FK
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    triggered_at: Mapped[Optional[datetime]] = mapped_column()
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self) -> str:
        return f"<PriceAlert part={self.part_id} target={self.target_price}>"
