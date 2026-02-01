import { describe, it, expect } from 'vitest';
import { CompatibilityChecker } from '../src/services/compatibility.js';

// Helper to create mock parts
function mockPart(id: number, category: string, specs: Record<string, string>) {
  return {
    id,
    manufacturer: 'Test',
    model: 'Model',
    fullName: `Test ${category}`,
    categoryId: 1,
    imageUrl: null,
    createdAt: new Date(),
    updatedAt: new Date(),
    category: { slug: category },
    specs: Object.entries(specs).map(([key, value], i) => ({
      id: i,
      partId: id,
      key,
      value,
      unit: null,
    })),
  };
}

describe('CompatibilityChecker', () => {
  const checker = new CompatibilityChecker();

  describe('CPU-Motherboard socket check', () => {
    it('passes when sockets match', () => {
      const cpu = mockPart(1, 'cpu', { socket: 'AM5' });
      const mobo = mockPart(2, 'motherboard', { socket: 'AM5' });

      const result = checker.checkPair(cpu, mobo);

      expect(result.compatible).toBe(true);
      expect(result.issues).toHaveLength(0);
    });

    it('fails when sockets mismatch', () => {
      const cpu = mockPart(1, 'cpu', { socket: 'LGA1700' });
      const mobo = mockPart(2, 'motherboard', { socket: 'AM5' });

      const result = checker.checkPair(cpu, mobo);

      expect(result.compatible).toBe(false);
      expect(result.issues).toHaveLength(1);
      expect(result.issues[0].severity).toBe('error');
      expect(result.issues[0].message).toContain('socket');
    });
  });

  describe('RAM-Motherboard type check', () => {
    it('passes when RAM types match', () => {
      const ram = mockPart(1, 'ram', { type: 'DDR5' });
      const mobo = mockPart(2, 'motherboard', { memory_type: 'DDR5' });

      const result = checker.checkPair(ram, mobo);

      expect(result.compatible).toBe(true);
      expect(result.issues).toHaveLength(0);
    });

    it('fails when RAM types mismatch', () => {
      const ram = mockPart(1, 'ram', { type: 'DDR4' });
      const mobo = mockPart(2, 'motherboard', { memory_type: 'DDR5' });

      const result = checker.checkPair(ram, mobo);

      expect(result.compatible).toBe(false);
      expect(result.issues).toHaveLength(1);
      expect(result.issues[0].message).toContain('DDR4');
    });
  });

  describe('Full build check', () => {
    it('passes with all compatible parts', () => {
      const cpu = mockPart(1, 'cpu', { socket: 'AM5' });
      const mobo = mockPart(2, 'motherboard', { socket: 'AM5', memory_type: 'DDR5' });
      const ram = mockPart(3, 'ram', { type: 'DDR5' });

      const result = checker.checkBuild([cpu, mobo, ram]);

      expect(result.compatible).toBe(true);
      expect(result.issues).toHaveLength(0);
    });

    it('fails with incompatible CPU', () => {
      const cpu = mockPart(1, 'cpu', { socket: 'LGA1700' });
      const mobo = mockPart(2, 'motherboard', { socket: 'AM5', memory_type: 'DDR5' });
      const ram = mockPart(3, 'ram', { type: 'DDR5' });

      const result = checker.checkBuild([cpu, mobo, ram]);

      expect(result.compatible).toBe(false);
      expect(result.issues.length).toBeGreaterThanOrEqual(1);
    });

    it('handles empty build', () => {
      const result = checker.checkBuild([]);

      expect(result.compatible).toBe(true);
      expect(result.issues).toHaveLength(0);
    });

    it('handles single part', () => {
      const cpu = mockPart(1, 'cpu', { socket: 'AM5' });

      const result = checker.checkBuild([cpu]);

      expect(result.compatible).toBe(true);
      expect(result.issues).toHaveLength(0);
    });
  });

  describe('PSU wattage check', () => {
    it('passes with adequate PSU', () => {
      const cpu = mockPart(1, 'cpu', { tdp: '170' });
      const gpu = mockPart(2, 'gpu', { tdp: '320' });
      const psu = mockPart(3, 'psu', { wattage: '850' });

      const result = checker.checkBuild([cpu, gpu, psu]);

      // 490W TDP, 850W PSU = plenty of headroom
      expect(result.compatible).toBe(true);
    });

    it('warns with tight PSU', () => {
      const cpu = mockPart(1, 'cpu', { tdp: '170' });
      const gpu = mockPart(2, 'gpu', { tdp: '450' });
      const psu = mockPart(3, 'psu', { wattage: '650' });

      const result = checker.checkBuild([cpu, gpu, psu]);

      // 620W TDP, needs 744W recommended, 650W PSU = warning
      const psuWarning = result.issues.find(i => 
        i.message.toLowerCase().includes('psu') || i.message.toLowerCase().includes('watt')
      );
      expect(psuWarning).toBeDefined();
      expect(psuWarning?.severity).toBe('warning');
    });
  });
});
