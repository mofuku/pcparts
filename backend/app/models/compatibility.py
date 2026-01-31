"""Compatibility rule models."""

from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CompatibilityRule(Base):
    """
    Rules for checking part compatibility.
    
    Rules are evaluated as simple expressions against part specs.
    
    Examples:
        - CPU socket must match motherboard socket
        - RAM type must match motherboard support
        - Total wattage must be <= PSU capacity
        - GPU length must fit case clearance
    
    Rule types:
        - "match": spec values must be equal (cpu.socket == mobo.socket)
        - "lte": left spec <= right spec (gpu.length <= case.gpu_clearance)
        - "gte": left spec >= right spec (psu.wattage >= build.total_tdp)
        - "in": left spec in right spec list (ram.type in mobo.ram_support)
    
    This is MVP. Future: DSL or rule engine for complex rules.
    """

    __tablename__ = "compatibility_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Rule identity
    name: Mapped[str] = mapped_column(String(100))  # "CPU-Motherboard Socket"
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Categories involved
    category_a: Mapped[str] = mapped_column(String(50), index=True)  # "cpu"
    category_b: Mapped[str] = mapped_column(String(50), index=True)  # "motherboard"
    
    # Rule definition
    rule_type: Mapped[str] = mapped_column(String(20))  # "match", "lte", "gte", "in"
    spec_a: Mapped[str] = mapped_column(String(50))  # "socket"
    spec_b: Mapped[str] = mapped_column(String(50))  # "socket"
    
    # Error messaging
    error_message: Mapped[str] = mapped_column(String(200))  # "CPU socket doesn't match motherboard"
    severity: Mapped[str] = mapped_column(String(20), default="error")  # "error", "warning"
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"<CompatibilityRule {self.name}>"
