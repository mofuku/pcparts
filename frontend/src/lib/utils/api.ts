/**
 * API client for PCParts backend
 * 
 * All API calls go through this module for consistency.
 * TODO: Replace mock data with real API calls once backend is ready.
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: unknown;
  headers?: Record<string, string>;
}

async function apiCall<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {} } = options;
  
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    },
    body: body ? JSON.stringify(body) : undefined
  });
  
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  
  return res.json();
}

// Part types
export interface Part {
  id: string;
  name: string;
  category: string;
  specs: Record<string, string>;
  prices: Price[];
  priceHistory: PricePoint[];
}

export interface Price {
  retailer: string;
  price: number;
  stock: 'In Stock' | 'Low Stock' | 'Out of Stock';
  url: string;
}

export interface PricePoint {
  date: string;
  price: number;
  retailer: string;
}

export interface SearchResult {
  id: string;
  name: string;
  category: string;
  specs: string;
  priceRange: { min: number; max: number };
  retailers: number;
  perfScore: number;
}

// API functions
export const api = {
  // Search parts
  search: (query: string, filters?: Record<string, unknown>) => 
    apiCall<{ results: SearchResult[]; total: number }>(`/parts/search?q=${encodeURIComponent(query)}`),
  
  // Get part details
  getPart: (id: string) => 
    apiCall<Part>(`/parts/${id}`),
  
  // Get price history
  getPriceHistory: (partId: string, days: number = 90) =>
    apiCall<PricePoint[]>(`/parts/${partId}/history?days=${days}`),
  
  // Get deals
  getDeals: (limit: number = 10) =>
    apiCall<SearchResult[]>(`/deals?limit=${limit}`),
  
  // Check compatibility
  checkCompatibility: (partIds: string[]) =>
    apiCall<{ compatible: boolean; warnings: string[]; errors: string[] }>('/compatibility/check', {
      method: 'POST',
      body: { partIds }
    }),
  
  // Create price alert
  createAlert: (partId: string, targetPrice: number, email: string) =>
    apiCall<{ id: string }>('/alerts', {
      method: 'POST',
      body: { partId, targetPrice, email }
    })
};

export default api;
