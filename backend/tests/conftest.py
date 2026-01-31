"""Pytest fixtures for PCParts backend tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
# Import all models to register them with Base
from app.models import Category, Part, PartSpec, Retailer, Price, Build, BuildItem, CompatibilityRule


@pytest.fixture
def db_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine):
    """Create a database session for testing."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_cpu(db_session):
    """Create a sample CPU part."""
    from app.models.parts import Category, Part, PartSpec
    
    # Create category
    cpu_cat = Category(slug="cpu", name="CPU")
    db_session.add(cpu_cat)
    db_session.flush()
    
    # Create part
    cpu = Part(
        manufacturer="AMD",
        model="Ryzen 5 7600X",
        full_name="AMD Ryzen 5 7600X",
        category_id=cpu_cat.id,
    )
    db_session.add(cpu)
    db_session.flush()
    
    # Add specs
    specs = [
        PartSpec(part_id=cpu.id, key="socket", value="AM5"),
        PartSpec(part_id=cpu.id, key="cores", value="6"),
        PartSpec(part_id=cpu.id, key="threads", value="12"),
        PartSpec(part_id=cpu.id, key="base_clock", value="4.7", unit="GHz"),
        PartSpec(part_id=cpu.id, key="tdp", value="105", unit="W"),
        PartSpec(part_id=cpu.id, key="memory_type", value="DDR5"),
    ]
    db_session.add_all(specs)
    db_session.commit()
    
    return cpu


@pytest.fixture
def sample_motherboard(db_session):
    """Create a sample motherboard part."""
    from app.models.parts import Category, Part, PartSpec
    
    # Get or create category
    mobo_cat = db_session.query(Category).filter_by(slug="motherboard").first()
    if not mobo_cat:
        mobo_cat = Category(slug="motherboard", name="Motherboard")
        db_session.add(mobo_cat)
        db_session.flush()
    
    mobo = Part(
        manufacturer="ASUS",
        model="ROG STRIX X670E-E",
        full_name="ASUS ROG STRIX X670E-E Gaming WiFi",
        category_id=mobo_cat.id,
    )
    db_session.add(mobo)
    db_session.flush()
    
    specs = [
        PartSpec(part_id=mobo.id, key="socket", value="AM5"),
        PartSpec(part_id=mobo.id, key="chipset", value="X670E"),
        PartSpec(part_id=mobo.id, key="form_factor", value="ATX"),
        PartSpec(part_id=mobo.id, key="memory_type", value="DDR5"),
        PartSpec(part_id=mobo.id, key="memory_slots", value="4"),
        PartSpec(part_id=mobo.id, key="max_memory", value="128", unit="GB"),
    ]
    db_session.add_all(specs)
    db_session.commit()
    
    return mobo


@pytest.fixture
def sample_ram(db_session):
    """Create a sample RAM part."""
    from app.models.parts import Category, Part, PartSpec
    
    ram_cat = db_session.query(Category).filter_by(slug="ram").first()
    if not ram_cat:
        ram_cat = Category(slug="ram", name="RAM")
        db_session.add(ram_cat)
        db_session.flush()
    
    ram = Part(
        manufacturer="G.Skill",
        model="Trident Z5 RGB",
        full_name="G.Skill Trident Z5 RGB 32GB DDR5-6000",
        category_id=ram_cat.id,
    )
    db_session.add(ram)
    db_session.flush()
    
    specs = [
        PartSpec(part_id=ram.id, key="type", value="DDR5"),
        PartSpec(part_id=ram.id, key="capacity", value="32", unit="GB"),
        PartSpec(part_id=ram.id, key="speed", value="6000", unit="MHz"),
        PartSpec(part_id=ram.id, key="modules", value="2"),
        PartSpec(part_id=ram.id, key="cas_latency", value="30"),
    ]
    db_session.add_all(specs)
    db_session.commit()
    
    return ram


@pytest.fixture
def incompatible_cpu(db_session):
    """Create a CPU with Intel socket (incompatible with AMD motherboard)."""
    from app.models.parts import Category, Part, PartSpec
    
    cpu_cat = db_session.query(Category).filter_by(slug="cpu").first()
    if not cpu_cat:
        cpu_cat = Category(slug="cpu", name="CPU")
        db_session.add(cpu_cat)
        db_session.flush()
    
    cpu = Part(
        manufacturer="Intel",
        model="Core i7-14700K",
        full_name="Intel Core i7-14700K",
        category_id=cpu_cat.id,
    )
    db_session.add(cpu)
    db_session.flush()
    
    specs = [
        PartSpec(part_id=cpu.id, key="socket", value="LGA1700"),
        PartSpec(part_id=cpu.id, key="cores", value="20"),
        PartSpec(part_id=cpu.id, key="tdp", value="125", unit="W"),
        PartSpec(part_id=cpu.id, key="memory_type", value="DDR5"),
    ]
    db_session.add_all(specs)
    db_session.commit()
    
    return cpu


@pytest.fixture
def ddr4_ram(db_session):
    """Create DDR4 RAM (incompatible with DDR5 motherboard)."""
    from app.models.parts import Category, Part, PartSpec
    
    ram_cat = db_session.query(Category).filter_by(slug="ram").first()
    if not ram_cat:
        ram_cat = Category(slug="ram", name="RAM")
        db_session.add(ram_cat)
        db_session.flush()
    
    ram = Part(
        manufacturer="Corsair",
        model="Vengeance LPX",
        full_name="Corsair Vengeance LPX 32GB DDR4-3200",
        category_id=ram_cat.id,
    )
    db_session.add(ram)
    db_session.flush()
    
    specs = [
        PartSpec(part_id=ram.id, key="type", value="DDR4"),
        PartSpec(part_id=ram.id, key="capacity", value="32", unit="GB"),
        PartSpec(part_id=ram.id, key="speed", value="3200", unit="MHz"),
    ]
    db_session.add_all(specs)
    db_session.commit()
    
    return ram
