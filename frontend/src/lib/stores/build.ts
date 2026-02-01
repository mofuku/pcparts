import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export interface BuildPart {
  id: string;
  name: string;
  category: string;
  price: number;
  specs: Record<string, string>;
}

export interface Build {
  id: string;
  name: string;
  parts: Partial<Record<ComponentType, BuildPart>>;
  createdAt: Date;
  updatedAt: Date;
}

export type ComponentType = 
  | 'cpu'
  | 'cpu-cooler'
  | 'gpu'
  | 'motherboard'
  | 'ram'
  | 'storage'
  | 'psu'
  | 'case';

function createBuildStore() {
  const storedBuild = browser ? localStorage.getItem('pcparts-build') : null;
  const initial: Build = storedBuild 
    ? JSON.parse(storedBuild)
    : {
        id: crypto.randomUUID(),
        name: 'My Build',
        parts: {},
        createdAt: new Date(),
        updatedAt: new Date()
      };
  
  const { subscribe, set, update } = writable<Build>(initial);
  
  // Persist to localStorage
  if (browser) {
    subscribe(value => {
      localStorage.setItem('pcparts-build', JSON.stringify(value));
    });
  }
  
  return {
    subscribe,
    
    addPart: (type: ComponentType, part: BuildPart) => {
      update(build => ({
        ...build,
        parts: { ...build.parts, [type]: part },
        updatedAt: new Date()
      }));
    },
    
    removePart: (type: ComponentType) => {
      update(build => {
        const { [type]: _, ...rest } = build.parts;
        return {
          ...build,
          parts: rest,
          updatedAt: new Date()
        };
      });
    },
    
    rename: (name: string) => {
      update(build => ({ ...build, name, updatedAt: new Date() }));
    },
    
    clear: () => {
      set({
        id: crypto.randomUUID(),
        name: 'My Build',
        parts: {},
        createdAt: new Date(),
        updatedAt: new Date()
      });
    },
    
    getTotal: (build: Build): number => {
      return Object.values(build.parts).reduce((sum, part) => sum + (part?.price || 0), 0);
    }
  };
}

export const buildStore = createBuildStore();
