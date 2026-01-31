"""
Seed the database with initial data.

Run: python -m scripts.seed
"""

import asyncio
from decimal import Decimal

from app.database import async_session, init_db
from app.models import Category, Retailer, Part, PartSpec, CompatibilityRule


async def seed():
    """Seed database with initial data."""
    await init_db()

    async with async_session() as db:
        # === Categories ===
        categories = [
            Category(slug="cpu", name="CPU / Processor", icon="🔲"),
            Category(slug="gpu", name="Graphics Card", icon="🎮"),
            Category(slug="motherboard", name="Motherboard", icon="📟"),
            Category(slug="ram", name="Memory (RAM)", icon="💾"),
            Category(slug="storage", name="Storage (SSD/HDD)", icon="💿"),
            Category(slug="psu", name="Power Supply", icon="⚡"),
            Category(slug="case", name="Case", icon="🖥️"),
            Category(slug="cooler", name="CPU Cooler", icon="❄️"),
            Category(slug="monitor", name="Monitor", icon="🖵"),
            Category(slug="peripheral", name="Peripherals", icon="⌨️"),
        ]
        db.add_all(categories)
        await db.flush()

        cat_map = {c.slug: c.id for c in categories}

        # === Retailers (US market to start) ===
        retailers = [
            Retailer(
                slug="amazon-us",
                name="Amazon US",
                base_url="https://www.amazon.com",
                country_code="US",
                currency="USD",
            ),
            Retailer(
                slug="newegg-us",
                name="Newegg",
                base_url="https://www.newegg.com",
                country_code="US",
                currency="USD",
            ),
            Retailer(
                slug="bhphoto",
                name="B&H Photo",
                base_url="https://www.bhphotovideo.com",
                country_code="US",
                currency="USD",
            ),
            Retailer(
                slug="bestbuy-us",
                name="Best Buy",
                base_url="https://www.bestbuy.com",
                country_code="US",
                currency="USD",
            ),
            Retailer(
                slug="microcenter",
                name="Micro Center",
                base_url="https://www.microcenter.com",
                country_code="US",
                currency="USD",
            ),
        ]
        db.add_all(retailers)

        # === Compatibility Rules ===
        rules = [
            CompatibilityRule(
                name="CPU-Motherboard Socket",
                description="CPU socket must match motherboard socket",
                category_a="cpu",
                category_b="motherboard",
                rule_type="match",
                spec_a="socket",
                spec_b="socket",
                error_message="CPU socket doesn't match motherboard. Check compatibility.",
                severity="error",
            ),
            CompatibilityRule(
                name="RAM-Motherboard Type",
                description="RAM type must be supported by motherboard",
                category_a="ram",
                category_b="motherboard",
                rule_type="match",
                spec_a="type",
                spec_b="ram_type",
                error_message="RAM type not supported by motherboard (e.g., DDR4 vs DDR5).",
                severity="error",
            ),
            CompatibilityRule(
                name="PSU Wattage",
                description="PSU should provide enough power",
                category_a="psu",
                category_b="gpu",  # Simplified - real check would sum all TDPs
                rule_type="gte",
                spec_a="wattage",
                spec_b="tdp",
                error_message="PSU may not provide enough power for this GPU. Consider upgrading.",
                severity="warning",
            ),
            CompatibilityRule(
                name="GPU Case Clearance",
                description="GPU must fit in case",
                category_a="gpu",
                category_b="case",
                rule_type="lte",
                spec_a="length",
                spec_b="gpu_clearance",
                error_message="GPU may be too long for this case. Check dimensions.",
                severity="warning",
            ),
        ]
        db.add_all(rules)

        # === Sample Parts (for testing) ===
        sample_parts = [
            (
                Part(
                    manufacturer="AMD",
                    model="Ryzen 5 7600X",
                    full_name="AMD Ryzen 5 7600X",
                    category_id=cat_map["cpu"],
                ),
                [
                    PartSpec(key="cores", value="6"),
                    PartSpec(key="threads", value="12"),
                    PartSpec(key="base_clock", value="4.7", unit="GHz"),
                    PartSpec(key="boost_clock", value="5.3", unit="GHz"),
                    PartSpec(key="socket", value="AM5"),
                    PartSpec(key="tdp", value="105", unit="W"),
                ],
            ),
            (
                Part(
                    manufacturer="Intel",
                    model="Core i5-13600K",
                    full_name="Intel Core i5-13600K",
                    category_id=cat_map["cpu"],
                ),
                [
                    PartSpec(key="cores", value="14"),
                    PartSpec(key="threads", value="20"),
                    PartSpec(key="base_clock", value="3.5", unit="GHz"),
                    PartSpec(key="boost_clock", value="5.1", unit="GHz"),
                    PartSpec(key="socket", value="LGA1700"),
                    PartSpec(key="tdp", value="125", unit="W"),
                ],
            ),
            (
                Part(
                    manufacturer="NVIDIA",
                    model="GeForce RTX 4070",
                    full_name="NVIDIA GeForce RTX 4070",
                    category_id=cat_map["gpu"],
                ),
                [
                    PartSpec(key="vram", value="12", unit="GB"),
                    PartSpec(key="memory_type", value="GDDR6X"),
                    PartSpec(key="tdp", value="200", unit="W"),
                    PartSpec(key="length", value="244", unit="mm"),
                ],
            ),
        ]

        for part, specs in sample_parts:
            db.add(part)
            await db.flush()
            for spec in specs:
                spec.part_id = part.id
                db.add(spec)

        await db.commit()
        print("✓ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
