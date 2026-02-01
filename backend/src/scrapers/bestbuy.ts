/**
 * Best Buy Products API adapter
 * Docs: https://bestbuyapis.github.io/api-documentation/
 */

const CATEGORY_MAP: Record<string, string> = {
  cpu: 'abcat0507002',
  gpu: 'abcat0507002',
  motherboard: 'abcat0507006',
  ram: 'abcat0503002',
  storage: 'pcmcat158900050001',
  psu: 'abcat0507009',
  case: 'abcat0507008',
  cooler: 'abcat0507005',
};

const SPEC_MAP: Record<string, string> = {
  'Number of Cores': 'cores',
  'Processor Speed': 'base_clock',
  'Socket Type': 'socket',
  'Memory Type': 'memory_type',
  'Memory Speed': 'speed',
  'Total Memory Capacity': 'capacity',
  'Graphics Memory': 'vram',
  'Form Factor': 'form_factor',
  'Wattage': 'wattage',
  'Chipset Brand': 'chipset',
};

export interface BestBuyProduct {
  sku: string;
  name: string;
  manufacturer: string;
  price: number;
  regularPrice: number;
  onSale: boolean;
  url: string;
  inStock: boolean;
  specs: Record<string, string>;
  categoryPath: string[];
}

interface RawProduct {
  sku: number;
  name: string;
  manufacturer: string;
  salePrice: number;
  regularPrice: number;
  onSale: boolean;
  url: string;
  categoryPath: Array<{ id: string; name: string }>;
  details: Array<{ name: string; value: string }>;
  inStoreAvailability: boolean;
  onlineAvailability: boolean;
}

interface ApiResponse {
  products: RawProduct[];
  total: number;
  from: number;
  to: number;
}

export class BestBuyAdapter {
  private apiKey: string;
  private baseUrl = 'https://api.bestbuy.com/v1';
  private requestsPerSecond: number;
  private lastRequestTime = 0;

  constructor(apiKey: string, requestsPerSecond = 5) {
    this.apiKey = apiKey;
    this.requestsPerSecond = requestsPerSecond;
  }

  getCategoryId(category: string): string {
    return CATEGORY_MAP[category] || category;
  }

  private async makeRequest(endpoint: string, params: Record<string, string> = {}): Promise<ApiResponse> {
    // Rate limiting
    const now = Date.now();
    const minInterval = 1000 / this.requestsPerSecond;
    const elapsed = now - this.lastRequestTime;
    if (elapsed < minInterval) {
      await new Promise(resolve => setTimeout(resolve, minInterval - elapsed));
    }

    const searchParams = new URLSearchParams({
      ...params,
      apiKey: this.apiKey,
      format: 'json',
    });

    const url = `${this.baseUrl}/${endpoint}?${searchParams}`;
    
    const response = await fetch(url);
    this.lastRequestTime = Date.now();

    if (!response.ok) {
      if (response.status === 429) {
        // Rate limited - wait and retry
        await new Promise(resolve => setTimeout(resolve, 5000));
        return this.makeRequest(endpoint, params);
      }
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  private parseProduct(raw: RawProduct): BestBuyProduct {
    const specs: Record<string, string> = {};
    
    for (const detail of raw.details || []) {
      const mappedKey = SPEC_MAP[detail.name];
      if (mappedKey) {
        // Clean up values (remove units)
        const cleanValue = detail.value.split(' ')[0];
        specs[mappedKey] = cleanValue;
      }
    }

    return {
      sku: String(raw.sku),
      name: raw.name,
      manufacturer: raw.manufacturer,
      price: raw.salePrice,
      regularPrice: raw.regularPrice,
      onSale: raw.onSale,
      url: raw.url,
      inStock: raw.onlineAvailability || raw.inStoreAvailability,
      specs,
      categoryPath: (raw.categoryPath || []).map(c => c.name),
    };
  }

  async fetchCategory(
    category: string,
    pageSize = 100,
    maxPages = 10
  ): Promise<BestBuyProduct[]> {
    const categoryId = this.getCategoryId(category);
    const products: BestBuyProduct[] = [];
    let page = 1;

    while (page <= maxPages) {
      const endpoint = `products(categoryPath.id=${categoryId})`;
      const params = {
        show: 'sku,name,manufacturer,salePrice,regularPrice,onSale,url,categoryPath,details,inStoreAvailability,onlineAvailability',
        pageSize: String(Math.min(pageSize, 100)),
        page: String(page),
      };

      const data = await this.makeRequest(endpoint, params);
      
      if (!data.products?.length) break;

      for (const raw of data.products) {
        products.push(this.parseProduct(raw));
      }

      if (data.to >= data.total) break;
      page++;
    }

    return products;
  }

  async search(query: string, limit = 20): Promise<BestBuyProduct[]> {
    const endpoint = `products(search=${encodeURIComponent(query)})`;
    const params = {
      show: 'sku,name,manufacturer,salePrice,regularPrice,onSale,url,categoryPath,details,inStoreAvailability,onlineAvailability',
      pageSize: String(Math.min(limit, 100)),
    };

    const data = await this.makeRequest(endpoint, params);
    return (data.products || []).map(p => this.parseProduct(p));
  }

  async getProduct(sku: string): Promise<BestBuyProduct | null> {
    const endpoint = `products(sku=${sku})`;
    const params = {
      show: 'sku,name,manufacturer,salePrice,regularPrice,onSale,url,categoryPath,details,inStoreAvailability,onlineAvailability',
    };

    const data = await this.makeRequest(endpoint, params);
    if (!data.products?.length) return null;

    return this.parseProduct(data.products[0]);
  }
}
