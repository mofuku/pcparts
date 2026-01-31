"""Build-related models."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.parts import Part


class Build(Base):
    """
    A user-created PC build (part list).
    
    Future: link to user_id when auth is added.
    """

    __tablename__ = "builds"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Identity
    name: Mapped[str] = mapped_column(String(200))  # "Gaming Beast 2024"
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Access
    share_token: Mapped[Optional[str]] = mapped_column(String(32), unique=True, index=True)
    is_public: Mapped[bool] = mapped_column(default=False)
    
    # Cached totals (updated on item changes)
    total_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    total_wattage: Mapped[Optional[int]] = mapped_column()
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # Relationships
    items: Mapped[list["BuildItem"]] = relationship(back_populates="build", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Build {self.name}>"


class BuildItem(Base):
    """
    A part in a build, with selected retailer preference.
    
    Quantity supports multi-GPU, multi-drive, etc.
    """

    __tablename__ = "build_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    build_id: Mapped[int] = mapped_column(ForeignKey("builds.id"), index=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts.id"))
    
    # Selection
    quantity: Mapped[int] = mapped_column(default=1)
    preferred_retailer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("retailers.id"))
    
    # Notes
    notes: Mapped[Optional[str]] = mapped_column(Text)  # "already owned", "on sale"

    # Relationships
    build: Mapped["Build"] = relationship(back_populates="items")
    part: Mapped["Part"] = relationship()

    def __repr__(self) -> str:
        return f"<BuildItem {self.part_id} x{self.quantity}>"
