import type { Part, PartSpec } from '../db/schema.js';

export interface CompatibilityIssue {
  severity: 'error' | 'warning' | 'info';
  message: string;
  parts: number[];
}

export interface CompatibilityResult {
  compatible: boolean;
  issues: CompatibilityIssue[];
}

interface PartWithSpecs extends Part {
  specs: PartSpec[];
  category?: { slug: string };
}

export class CompatibilityChecker {
  private getSpec(part: PartWithSpecs, key: string): string | null {
    const spec = part.specs.find(s => s.key === key);
    return spec?.value ?? null;
  }

  private getSpecNumeric(part: PartWithSpecs, key: string): number | null {
    const value = this.getSpec(part, key);
    if (!value) return null;
    const num = parseFloat(value);
    return isNaN(num) ? null : num;
  }

  checkPair(partA: PartWithSpecs, partB: PartWithSpecs): CompatibilityResult {
    const issues: CompatibilityIssue[] = [];
    
    const catA = partA.category?.slug;
    const catB = partB.category?.slug;
    const cats = new Set([catA, catB]);

    // CPU-Motherboard socket check
    if (cats.has('cpu') && cats.has('motherboard')) {
      const cpu = catA === 'cpu' ? partA : partB;
      const mobo = catA === 'motherboard' ? partA : partB;
      
      const cpuSocket = this.getSpec(cpu, 'socket');
      const moboSocket = this.getSpec(mobo, 'socket');
      
      if (cpuSocket && moboSocket && cpuSocket !== moboSocket) {
        issues.push({
          severity: 'error',
          message: `CPU socket ${cpuSocket} doesn't match motherboard socket ${moboSocket}`,
          parts: [cpu.id, mobo.id],
        });
      }
    }

    // RAM-Motherboard type check
    if (cats.has('ram') && cats.has('motherboard')) {
      const ram = catA === 'ram' ? partA : partB;
      const mobo = catA === 'motherboard' ? partA : partB;
      
      const ramType = this.getSpec(ram, 'type');
      const moboType = this.getSpec(mobo, 'memory_type');
      
      if (ramType && moboType && ramType !== moboType) {
        issues.push({
          severity: 'error',
          message: `RAM type ${ramType} doesn't match motherboard memory type ${moboType}`,
          parts: [ram.id, mobo.id],
        });
      }
    }

    const hasErrors = issues.some(i => i.severity === 'error');
    return { compatible: !hasErrors, issues };
  }

  checkBuild(parts: PartWithSpecs[]): CompatibilityResult {
    if (parts.length <= 1) {
      return { compatible: true, issues: [] };
    }

    const allIssues: CompatibilityIssue[] = [];

    // Check all pairs
    for (let i = 0; i < parts.length; i++) {
      for (let j = i + 1; j < parts.length; j++) {
        const result = this.checkPair(parts[i], parts[j]);
        allIssues.push(...result.issues);
      }
    }

    // PSU wattage check
    allIssues.push(...this.checkPsuWattage(parts));

    // Deduplicate
    const seen = new Set<string>();
    const uniqueIssues = allIssues.filter(issue => {
      const key = `${issue.severity}:${issue.message}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });

    const hasErrors = uniqueIssues.some(i => i.severity === 'error');
    return { compatible: !hasErrors, issues: uniqueIssues };
  }

  private checkPsuWattage(parts: PartWithSpecs[]): CompatibilityIssue[] {
    const issues: CompatibilityIssue[] = [];
    
    let psu: PartWithSpecs | null = null;
    let totalTdp = 0;

    for (const part of parts) {
      if (part.category?.slug === 'psu') {
        psu = part;
      } else {
        const tdp = this.getSpecNumeric(part, 'tdp');
        if (tdp) totalTdp += tdp;
      }
    }

    if (psu && totalTdp > 0) {
      const psuWattage = this.getSpecNumeric(psu, 'wattage');
      if (psuWattage) {
        const recommended = totalTdp * 1.2;

        if (psuWattage < totalTdp) {
          issues.push({
            severity: 'error',
            message: `PSU ${psuWattage}W is insufficient for ${totalTdp}W total TDP`,
            parts: [psu.id],
          });
        } else if (psuWattage < recommended) {
          issues.push({
            severity: 'warning',
            message: `PSU ${psuWattage}W may be tight for ${totalTdp}W TDP (recommended: ${Math.ceil(recommended)}W)`,
            parts: [psu.id],
          });
        }
      }
    }

    return issues;
  }
}
