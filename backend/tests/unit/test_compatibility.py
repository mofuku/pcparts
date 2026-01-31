"""
Tests for the compatibility checker.

TDD: These tests are written BEFORE the implementation.
They should all fail initially, then we implement to make them pass.
"""

import pytest


class TestCompatibilityChecker:
    """Test suite for CompatibilityChecker."""
    
    def test_compatible_cpu_motherboard_same_socket(
        self, db_session, sample_cpu, sample_motherboard
    ):
        """CPU and motherboard with same socket should be compatible."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_pair(sample_cpu, sample_motherboard)
        
        assert result.compatible is True
        assert len(result.issues) == 0
    
    def test_incompatible_cpu_motherboard_different_socket(
        self, db_session, incompatible_cpu, sample_motherboard
    ):
        """CPU and motherboard with different sockets should fail."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_pair(incompatible_cpu, sample_motherboard)
        
        assert result.compatible is False
        assert len(result.issues) == 1
        assert result.issues[0].severity == "error"
        assert "socket" in result.issues[0].message.lower()
    
    def test_compatible_ram_motherboard_same_type(
        self, db_session, sample_ram, sample_motherboard
    ):
        """DDR5 RAM on DDR5 motherboard should be compatible."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_pair(sample_ram, sample_motherboard)
        
        assert result.compatible is True
        assert len(result.issues) == 0
    
    def test_incompatible_ram_motherboard_different_type(
        self, db_session, ddr4_ram, sample_motherboard
    ):
        """DDR4 RAM on DDR5 motherboard should fail."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_pair(ddr4_ram, sample_motherboard)
        
        assert result.compatible is False
        assert len(result.issues) == 1
        assert "ddr" in result.issues[0].message.lower() or "memory" in result.issues[0].message.lower()
    
    def test_full_build_all_compatible(
        self, db_session, sample_cpu, sample_motherboard, sample_ram
    ):
        """A build with all compatible parts should pass."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        parts = [sample_cpu, sample_motherboard, sample_ram]
        result = checker.check_build(parts)
        
        assert result.compatible is True
        assert len(result.issues) == 0
    
    def test_full_build_one_incompatible(
        self, db_session, incompatible_cpu, sample_motherboard, sample_ram
    ):
        """A build with one incompatible part should fail."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        parts = [incompatible_cpu, sample_motherboard, sample_ram]
        result = checker.check_build(parts)
        
        assert result.compatible is False
        assert len(result.issues) >= 1
    
    def test_empty_build_is_compatible(self, db_session):
        """An empty build should be compatible (vacuously true)."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_build([])
        
        assert result.compatible is True
        assert len(result.issues) == 0
    
    def test_single_part_is_compatible(self, db_session, sample_cpu):
        """A build with a single part should be compatible."""
        from app.services.compatibility import CompatibilityChecker
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_build([sample_cpu])
        
        assert result.compatible is True
        assert len(result.issues) == 0


class TestPSUWattageCheck:
    """Test PSU wattage adequacy checks."""
    
    def test_psu_adequate_wattage(self, db_session):
        """PSU with enough wattage for the build should pass."""
        from app.models.parts import Category, Part, PartSpec
        from app.services.compatibility import CompatibilityChecker
        
        # Create PSU category
        psu_cat = Category(slug="psu", name="PSU")
        cpu_cat = Category(slug="cpu", name="CPU")
        gpu_cat = Category(slug="gpu", name="GPU")
        db_session.add_all([psu_cat, cpu_cat, gpu_cat])
        db_session.flush()
        
        # 850W PSU
        psu = Part(manufacturer="Corsair", model="RM850x", full_name="Corsair RM850x", category_id=psu_cat.id)
        db_session.add(psu)
        db_session.flush()
        db_session.add(PartSpec(part_id=psu.id, key="wattage", value="850", unit="W"))
        
        # 125W CPU
        cpu = Part(manufacturer="AMD", model="7950X", full_name="AMD Ryzen 9 7950X", category_id=cpu_cat.id)
        db_session.add(cpu)
        db_session.flush()
        db_session.add(PartSpec(part_id=cpu.id, key="tdp", value="170", unit="W"))
        
        # 350W GPU
        gpu = Part(manufacturer="NVIDIA", model="RTX 4080", full_name="NVIDIA RTX 4080", category_id=gpu_cat.id)
        db_session.add(gpu)
        db_session.flush()
        db_session.add(PartSpec(part_id=gpu.id, key="tdp", value="320", unit="W"))
        
        db_session.commit()
        
        # Total TDP = 170 + 320 = 490W
        # 850W PSU with 20% headroom = 680W max recommended
        # 490W < 680W, so should pass
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_build([cpu, gpu, psu])
        
        # Should be compatible (850W is enough for 490W)
        assert result.compatible is True
    
    def test_psu_inadequate_wattage_warning(self, db_session):
        """PSU with barely enough wattage should warn."""
        from app.models.parts import Category, Part, PartSpec
        from app.services.compatibility import CompatibilityChecker
        
        psu_cat = Category(slug="psu", name="PSU")
        cpu_cat = Category(slug="cpu", name="CPU")
        gpu_cat = Category(slug="gpu", name="GPU")
        db_session.add_all([psu_cat, cpu_cat, gpu_cat])
        db_session.flush()
        
        # 650W PSU
        psu = Part(manufacturer="EVGA", model="650 G6", full_name="EVGA 650 G6", category_id=psu_cat.id)
        db_session.add(psu)
        db_session.flush()
        db_session.add(PartSpec(part_id=psu.id, key="wattage", value="650", unit="W"))
        
        # 170W CPU
        cpu = Part(manufacturer="AMD", model="7950X", full_name="AMD Ryzen 9 7950X", category_id=cpu_cat.id)
        db_session.add(cpu)
        db_session.flush()
        db_session.add(PartSpec(part_id=cpu.id, key="tdp", value="170", unit="W"))
        
        # 450W GPU (RTX 4090)
        gpu = Part(manufacturer="NVIDIA", model="RTX 4090", full_name="NVIDIA RTX 4090", category_id=gpu_cat.id)
        db_session.add(gpu)
        db_session.flush()
        db_session.add(PartSpec(part_id=gpu.id, key="tdp", value="450", unit="W"))
        
        db_session.commit()
        
        # Total TDP = 170 + 450 = 620W
        # 650W PSU, recommended = 620 * 1.2 = 744W
        # Should warn (not error)
        
        checker = CompatibilityChecker(db_session)
        result = checker.check_build([cpu, gpu, psu])
        
        # Should have a warning about PSU
        psu_issues = [i for i in result.issues if "psu" in i.message.lower() or "watt" in i.message.lower()]
        assert len(psu_issues) >= 1
        assert psu_issues[0].severity == "warning"
