"""
Compatibility checking service.

Checks if PC parts are compatible with each other based on specs.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from app.models.parts import Part


@dataclass
class CompatibilityIssue:
    """A compatibility issue between parts."""
    
    severity: str  # "error", "warning", "info"
    message: str
    parts: list[int] = field(default_factory=list)  # Part IDs involved


@dataclass
class CompatibilityResult:
    """Result of a compatibility check."""
    
    compatible: bool
    issues: list[CompatibilityIssue] = field(default_factory=list)


class CompatibilityChecker:
    """
    Checks compatibility between PC parts.
    
    Rules:
    - CPU socket must match motherboard socket
    - RAM type must match motherboard memory_type
    - PSU wattage should be >= total TDP * 1.2
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_spec(self, part: "Part", key: str) -> Optional[str]:
        """Get a spec value from a part."""
        for spec in part.specs:
            if spec.key == key:
                return spec.value
        return None
    
    def get_spec_numeric(self, part: "Part", key: str) -> Optional[float]:
        """Get a numeric spec value from a part."""
        value = self.get_spec(part, key)
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None
    
    def check_pair(self, part_a: "Part", part_b: "Part") -> CompatibilityResult:
        """Check compatibility between two parts."""
        issues = []
        
        cat_a = part_a.category.slug
        cat_b = part_b.category.slug
        
        # CPU-Motherboard socket check
        if {cat_a, cat_b} == {"cpu", "motherboard"}:
            cpu = part_a if cat_a == "cpu" else part_b
            mobo = part_a if cat_a == "motherboard" else part_b
            
            cpu_socket = self.get_spec(cpu, "socket")
            mobo_socket = self.get_spec(mobo, "socket")
            
            if cpu_socket and mobo_socket and cpu_socket != mobo_socket:
                issues.append(CompatibilityIssue(
                    severity="error",
                    message=f"CPU socket {cpu_socket} doesn't match motherboard socket {mobo_socket}",
                    parts=[cpu.id, mobo.id],
                ))
        
        # RAM-Motherboard type check
        if {cat_a, cat_b} == {"ram", "motherboard"}:
            ram = part_a if cat_a == "ram" else part_b
            mobo = part_a if cat_a == "motherboard" else part_b
            
            ram_type = self.get_spec(ram, "type")
            mobo_type = self.get_spec(mobo, "memory_type")
            
            if ram_type and mobo_type and ram_type != mobo_type:
                issues.append(CompatibilityIssue(
                    severity="error",
                    message=f"RAM type {ram_type} doesn't match motherboard memory type {mobo_type}",
                    parts=[ram.id, mobo.id],
                ))
        
        compatible = len([i for i in issues if i.severity == "error"]) == 0
        return CompatibilityResult(compatible=compatible, issues=issues)
    
    def check_build(self, parts: list["Part"]) -> CompatibilityResult:
        """Check compatibility of an entire build."""
        if len(parts) <= 1:
            return CompatibilityResult(compatible=True, issues=[])
        
        all_issues = []
        
        # Check all pairs
        for i, part_a in enumerate(parts):
            for part_b in parts[i + 1:]:
                result = self.check_pair(part_a, part_b)
                all_issues.extend(result.issues)
        
        # PSU wattage check
        all_issues.extend(self._check_psu_wattage(parts))
        
        # Deduplicate issues
        seen = set()
        unique_issues = []
        for issue in all_issues:
            key = (issue.severity, issue.message)
            if key not in seen:
                seen.add(key)
                unique_issues.append(issue)
        
        compatible = len([i for i in unique_issues if i.severity == "error"]) == 0
        return CompatibilityResult(compatible=compatible, issues=unique_issues)
    
    def _check_psu_wattage(self, parts: list["Part"]) -> list[CompatibilityIssue]:
        """Check if PSU has adequate wattage for the build."""
        issues = []
        
        psu = None
        total_tdp = 0.0
        
        for part in parts:
            if part.category.slug == "psu":
                psu = part
            else:
                tdp = self.get_spec_numeric(part, "tdp")
                if tdp:
                    total_tdp += tdp
        
        if psu and total_tdp > 0:
            psu_wattage = self.get_spec_numeric(psu, "wattage")
            if psu_wattage:
                # Recommend 20% headroom
                recommended = total_tdp * 1.2
                
                if psu_wattage < total_tdp:
                    # Critical: PSU can't even handle the load
                    issues.append(CompatibilityIssue(
                        severity="error",
                        message=f"PSU {psu_wattage}W is insufficient for {total_tdp:.0f}W total TDP",
                        parts=[psu.id],
                    ))
                elif psu_wattage < recommended:
                    # Warning: PSU is cutting it close
                    issues.append(CompatibilityIssue(
                        severity="warning",
                        message=f"PSU {psu_wattage}W may be tight for {total_tdp:.0f}W TDP (recommended: {recommended:.0f}W)",
                        parts=[psu.id],
                    ))
        
        return issues
