"""Prices and retailers API."""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Price, Retailer
from app.schemas.prices import (
    PriceCreate,
    PriceResponse,
    PriceHistory,
    PricePoint,
    RetailerCreate,
    RetailerResponse,
)

router = APIRouter()


# === Retailers ===


@router.get("/retailers", response_model=list[RetailerResponse])
async def list_retailers(
    country: str | None = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """List retailers, optionally filtered by country."""
    query = select(Retailer)

    if country:
        query = query.where(Retailer.country_code == country.upper())
    if active_only:
        query = query.where(Retailer.is_active == True)

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/retailers", response_model=RetailerResponse, status_code=201)
async def create_retailer(data: RetailerCreate, db: AsyncSession = Depends(get_db)):
    """Register a new retailer."""
    retailer = Retailer(**data.model_dump())
    db.add(retailer)
    await db.flush()
    await db.refresh(retailer)
    return retailer


# === Prices ===


@router.post("", response_model=PriceResponse, status_code=201)
async def record_price(data: PriceCreate, db: AsyncSession = Depends(get_db)):
    """
    Record a price (called by scrapers).
    
    This creates a new price snapshot for history tracking.
    """
    price = Price(**data.model_dump())
    db.add(price)
    await db.flush()
    await db.refresh(price)
    return price


@router.get("/history/{part_id}", response_model=list[PriceHistory])
async def get_price_history(
    part_id: int,
    retailer_id: int | None = None,
    days: int = Query(default=30, le=365),
    db: AsyncSession = Depends(get_db),
):
    """
    Get price history for a part.
    
    Returns history from all retailers unless retailer_id is specified.
    """
    since = datetime.utcnow() - timedelta(days=days)

    query = (
        select(Price)
        .options(selectinload(Price.retailer))
        .where(Price.part_id == part_id, Price.scraped_at >= since)
        .order_by(Price.retailer_id, Price.scraped_at)
    )

    if retailer_id:
        query = query.where(Price.retailer_id == retailer_id)

    result = await db.execute(query)
    prices = result.scalars().all()

    # Group by retailer
    from itertools import groupby

    histories = []
    for retailer_id, group in groupby(prices, key=lambda p: p.retailer_id):
        group_list = list(group)
        if not group_list:
            continue

        retailer = group_list[0].retailer
        points = [
            PricePoint(price=p.price, in_stock=p.in_stock, scraped_at=p.scraped_at)
            for p in group_list
        ]

        histories.append(
            PriceHistory(
                part_id=part_id,
                retailer_id=retailer_id,
                retailer_name=retailer.name,
                currency=retailer.currency,
                history=points,
                lowest_price=min(p.price for p in points),
                highest_price=max(p.price for p in points),
                current_price=points[-1].price if points else None,
            )
        )

    return histories


@router.get("/compare/{part_id}")
async def compare_prices(part_id: int, db: AsyncSession = Depends(get_db)):
    """
    Compare current prices across all retailers for a part.
    
    Returns prices sorted from lowest to highest.
    """
    # Get latest price from each retailer
    latest_subq = (
        select(Price.retailer_id, func.max(Price.scraped_at).label("max_scraped"))
        .where(Price.part_id == part_id)
        .group_by(Price.retailer_id)
        .subquery()
    )

    result = await db.execute(
        select(Price)
        .options(selectinload(Price.retailer))
        .join(
            latest_subq,
            (Price.retailer_id == latest_subq.c.retailer_id)
            & (Price.scraped_at == latest_subq.c.max_scraped),
        )
        .where(Price.part_id == part_id)
        .order_by(Price.price)
    )
    prices = result.scalars().all()

    return {
        "part_id": part_id,
        "prices": [
            {
                "retailer": p.retailer.name,
                "price": float(p.price),
                "currency": p.currency,
                "in_stock": p.in_stock,
                "url": p.product_url,
                "scraped_at": p.scraped_at.isoformat(),
            }
            for p in prices
        ],
        "lowest": {
            "retailer": prices[0].retailer.name,
            "price": float(prices[0].price),
        }
        if prices
        else None,
    }
