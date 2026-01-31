"""Part-related models."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.prices import Price


class Category(Base):
    """Part categories: CPU, GPU, RAM, Motherboard, etc."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # "cpu", "gpu"
    name: Mapped[str] = mapped_column(String(100))  # "CPU", "Graphics Card"
    icon: Mapped[Optional[str]] = mapped_column(String(50))  # emoji or icon name

    # Relationships
    parts: Mapped[list["Part"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.slug}>"


class Part(Base):
    """
    A PC component (e.g., AMD Ryzen 5 7600X).
    
    Parts are deduplicated by manufacturer + model.
    Prices come from retailers via the Price model.
    """

    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Identity
    manufacturer: Mapped[str] = mapped_column(String(100), index=True)
    model: Mapped[str] = mapped_column(String(200))
    full_name: Mapped[str] = mapped_column(String(300))  # "AMD Ryzen 5 7600X"
    
    # Classification
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    
    # Optional metadata
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # Relationships
    category: Mapped["Category"] = relationship(back_populates="parts")
    specs: Mapped[list["PartSpec"]] = relationship(back_populates="part", cascade="all, delete-orphan")
    prices: Mapped[list["Price"]] = relationship(back_populates="part", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Part {self.full_name}>"


class PartSpec(Base):
    """
    Dynamic key-value specifications for parts.
    
    Examples:
        - CPU: cores=6, threads=12, base_clock=4.7, socket=AM5, tdp=105
        - GPU: vram=12, memory_type=GDDR6X, cuda_cores=8704
        - RAM: capacity=32, speed=6000, type=DDR5, cas_latency=30
    
    This flexible schema handles any part type without schema changes.
    """

    __tablename__ = "part_specs"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts.id"), index=True)
    
    key: Mapped[str] = mapped_column(String(50))  # "cores", "vram", "socket"
    value: Mapped[str] = mapped_column(String(200))  # stored as string, parsed as needed
    unit: Mapped[Optional[str]] = mapped_column(String(20))  # "GB", "MHz", "W"

    # Relationships
    part: Mapped["Part"] = relationship(back_populates="specs")

    def __repr__(self) -> str:
        return f"<PartSpec {self.key}={self.value}>"
