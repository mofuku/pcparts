"""Build schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.parts import PartWithPrices


class BuildItemCreate(BaseModel):
    """Add item to a build."""

    part_id: int
    quantity: int = 1
    preferred_retailer_id: int | None = None
    notes: str | None = None


class BuildItemResponse(BaseModel):
    """Build item response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    part_id: int
    quantity: int
    preferred_retailer_id: int | None
    notes: str | None


class BuildItemWithPart(BuildItemResponse):
    """Build item with full part info."""

    part: PartWithPrices


class BuildCreate(BaseModel):
    """Create a new build."""

    name: str
    description: str | None = None
    is_public: bool = False


class BuildResponse(BaseModel):
    """Build response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    share_token: str | None
    is_public: bool
    total_price: Decimal | None
    total_wattage: int | None
    created_at: datetime
    updated_at: datetime


class BuildWithItems(BuildResponse):
    """Build with all items and prices."""

    items: list[BuildItemWithPart] = []


class CompatibilityIssue(BaseModel):
    """A compatibility issue found in a build."""

    rule_name: str
    severity: str  # "error" or "warning"
    message: str
    parts_involved: list[str]  # part full_names


class CompatibilityCheck(BaseModel):
    """Result of checking build compatibility."""

    build_id: int
    is_compatible: bool
    issues: list[CompatibilityIssue] = []
