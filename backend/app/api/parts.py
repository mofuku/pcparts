"""Parts and categories API."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Category, Part, PartSpec, Price
from app.schemas.parts import (
    CategoryCreate,
    CategoryResponse,
    PartCreate,
    PartResponse,
    PartWithPrices,
    PartPriceInfo,
    PartSpecSchema,
)

router = APIRouter()


# === Categories ===


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """List all part categories."""
    result = await db.execute(select(Category))
    return result.scalars().all()


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """Create a new category."""
    category = Category(**data.model_dump())
    db.add(category)
    await db.flush()
    await db.refresh(category)
    return category


# === Parts ===


@router.get("", response_model=list[PartResponse])
async def list_parts(
    category: str | None = None,
    manufacturer: str | None = None,
    search: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    List parts with optional filters.
    
    - **category**: Filter by category slug (e.g., "cpu", "gpu")
    - **manufacturer**: Filter by manufacturer name
    - **search**: Search in full_name
    """
    query = select(Part).options(selectinload(Part.specs))

    if category:
        query = query.join(Category).where(Category.slug == category)
    if manufacturer:
        query = query.where(Part.manufacturer.ilike(f"%{manufacturer}%"))
    if search:
        query = query.where(Part.full_name.ilike(f"%{search}%"))

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    parts = result.scalars().all()

    # Convert specs to schema
    return [
        PartResponse(
            **{k: v for k, v in part.__dict__.items() if not k.startswith("_")},
            specs=[PartSpecSchema(key=s.key, value=s.value, unit=s.unit) for s in part.specs],
        )
        for part in parts
    ]


@router.get("/{part_id}", response_model=PartWithPrices)
async def get_part(part_id: int, db: AsyncSession = Depends(get_db)):
    """Get a part with latest prices from all retailers."""
    result = await db.execute(
        select(Part)
        .options(selectinload(Part.specs), selectinload(Part.category))
        .where(Part.id == part_id)
    )
    part = result.scalar_one_or_none()

    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    # Get latest price from each retailer
    from sqlalchemy import func, and_

    latest_prices_subq = (
        select(Price.retailer_id, func.max(Price.scraped_at).label("max_scraped"))
        .where(Price.part_id == part_id)
        .group_by(Price.retailer_id)
        .subquery()
    )

    prices_result = await db.execute(
        select(Price)
        .options(selectinload(Price.retailer))
        .join(
            latest_prices_subq,
            and_(
                Price.retailer_id == latest_prices_subq.c.retailer_id,
                Price.scraped_at == latest_prices_subq.c.max_scraped,
            ),
        )
        .where(Price.part_id == part_id)
    )
    prices = prices_result.scalars().all()

    price_infos = [
        PartPriceInfo(
            retailer_slug=p.retailer.slug,
            retailer_name=p.retailer.name,
            price=p.price,
            currency=p.currency,
            in_stock=p.in_stock,
            product_url=p.product_url,
            scraped_at=p.scraped_at,
        )
        for p in prices
    ]

    lowest = min((p.price for p in price_infos if p.in_stock), default=None)

    return PartWithPrices(
        **{k: v for k, v in part.__dict__.items() if not k.startswith("_")},
        specs=[PartSpecSchema(key=s.key, value=s.value, unit=s.unit) for s in part.specs],
        category=CategoryResponse.model_validate(part.category) if part.category else None,
        prices=price_infos,
        lowest_price=lowest,
    )


@router.post("", response_model=PartResponse, status_code=201)
async def create_part(data: PartCreate, db: AsyncSession = Depends(get_db)):
    """Create a new part."""
    specs_data = data.specs
    part_data = data.model_dump(exclude={"specs"})

    part = Part(**part_data)
    db.add(part)
    await db.flush()

    for spec in specs_data:
        db.add(PartSpec(part_id=part.id, **spec.model_dump()))

    await db.refresh(part)
    return PartResponse(
        **{k: v for k, v in part.__dict__.items() if not k.startswith("_")},
        specs=specs_data,
    )
