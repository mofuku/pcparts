"""Builds API."""

import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Build, BuildItem, Part, CompatibilityRule, PartSpec
from app.schemas.builds import (
    BuildCreate,
    BuildResponse,
    BuildItemCreate,
    BuildWithItems,
    CompatibilityCheck,
    CompatibilityIssue,
    BuildItemResponse,
)

router = APIRouter()


@router.post("", response_model=BuildResponse, status_code=201)
async def create_build(data: BuildCreate, db: AsyncSession = Depends(get_db)):
    """Create a new build."""
    build = Build(
        **data.model_dump(),
        share_token=secrets.token_urlsafe(16) if data.is_public else None,
    )
    db.add(build)
    await db.flush()
    await db.refresh(build)
    return build


@router.get("", response_model=list[BuildResponse])
async def list_builds(
    public_only: bool = False,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """List builds."""
    query = select(Build)
    if public_only:
        query = query.where(Build.is_public == True)
    query = query.limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{build_id}", response_model=BuildWithItems)
async def get_build(build_id: int, db: AsyncSession = Depends(get_db)):
    """Get a build with all items and prices."""
    result = await db.execute(
        select(Build).options(selectinload(Build.items)).where(Build.id == build_id)
    )
    build = result.scalar_one_or_none()

    if not build:
        raise HTTPException(status_code=404, detail="Build not found")

    # Load parts with prices for each item
    # This is simplified - in production, use a more efficient query
    items_with_parts = []
    for item in build.items:
        part_result = await db.execute(
            select(Part)
            .options(selectinload(Part.specs), selectinload(Part.category))
            .where(Part.id == item.part_id)
        )
        part = part_result.scalar_one_or_none()

        items_with_parts.append(
            {
                "id": item.id,
                "part_id": item.part_id,
                "quantity": item.quantity,
                "preferred_retailer_id": item.preferred_retailer_id,
                "notes": item.notes,
                "part": part,  # Will be converted by pydantic
            }
        )

    return BuildWithItems(
        **{k: v for k, v in build.__dict__.items() if not k.startswith("_") and k != "items"},
        items=items_with_parts,
    )


@router.get("/share/{token}", response_model=BuildWithItems)
async def get_shared_build(token: str, db: AsyncSession = Depends(get_db)):
    """Get a build by its share token."""
    result = await db.execute(
        select(Build).options(selectinload(Build.items)).where(Build.share_token == token)
    )
    build = result.scalar_one_or_none()

    if not build:
        raise HTTPException(status_code=404, detail="Build not found")

    # Same as get_build, return with items
    return await get_build(build.id, db)


@router.post("/{build_id}/items", response_model=BuildItemResponse, status_code=201)
async def add_item(build_id: int, data: BuildItemCreate, db: AsyncSession = Depends(get_db)):
    """Add a part to a build."""
    # Verify build exists
    result = await db.execute(select(Build).where(Build.id == build_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Build not found")

    # Verify part exists
    result = await db.execute(select(Part).where(Part.id == data.part_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Part not found")

    item = BuildItem(build_id=build_id, **data.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)

    # TODO: Update build totals

    return item


@router.delete("/{build_id}/items/{item_id}", status_code=204)
async def remove_item(build_id: int, item_id: int, db: AsyncSession = Depends(get_db)):
    """Remove a part from a build."""
    result = await db.execute(
        select(BuildItem).where(BuildItem.id == item_id, BuildItem.build_id == build_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)


@router.get("/{build_id}/compatibility", response_model=CompatibilityCheck)
async def check_compatibility(build_id: int, db: AsyncSession = Depends(get_db)):
    """
    Check build compatibility.
    
    Evaluates all active compatibility rules against the parts in the build.
    """
    # Get build with items
    result = await db.execute(
        select(Build).options(selectinload(Build.items)).where(Build.id == build_id)
    )
    build = result.scalar_one_or_none()

    if not build:
        raise HTTPException(status_code=404, detail="Build not found")

    # Get all parts with specs
    part_ids = [item.part_id for item in build.items]
    if not part_ids:
        return CompatibilityCheck(build_id=build_id, is_compatible=True, issues=[])

    parts_result = await db.execute(
        select(Part)
        .options(selectinload(Part.specs), selectinload(Part.category))
        .where(Part.id.in_(part_ids))
    )
    parts = {p.id: p for p in parts_result.scalars().all()}

    # Get active rules
    rules_result = await db.execute(
        select(CompatibilityRule).where(CompatibilityRule.is_active == True)
    )
    rules = rules_result.scalars().all()

    # Check each rule
    issues = []

    for rule in rules:
        # Find parts matching each category
        parts_a = [p for p in parts.values() if p.category and p.category.slug == rule.category_a]
        parts_b = [p for p in parts.values() if p.category and p.category.slug == rule.category_b]

        if not parts_a or not parts_b:
            continue  # Rule doesn't apply if categories missing

        for part_a in parts_a:
            spec_a = next((s.value for s in part_a.specs if s.key == rule.spec_a), None)
            if spec_a is None:
                continue

            for part_b in parts_b:
                spec_b = next((s.value for s in part_b.specs if s.key == rule.spec_b), None)
                if spec_b is None:
                    continue

                # Evaluate rule
                is_ok = False
                if rule.rule_type == "match":
                    is_ok = spec_a == spec_b
                elif rule.rule_type == "lte":
                    try:
                        is_ok = float(spec_a) <= float(spec_b)
                    except ValueError:
                        pass
                elif rule.rule_type == "gte":
                    try:
                        is_ok = float(spec_a) >= float(spec_b)
                    except ValueError:
                        pass
                elif rule.rule_type == "in":
                    is_ok = spec_a in spec_b.split(",")

                if not is_ok:
                    issues.append(
                        CompatibilityIssue(
                            rule_name=rule.name,
                            severity=rule.severity,
                            message=rule.error_message,
                            parts_involved=[part_a.full_name, part_b.full_name],
                        )
                    )

    has_errors = any(i.severity == "error" for i in issues)

    return CompatibilityCheck(
        build_id=build_id,
        is_compatible=not has_errors,
        issues=issues,
    )
