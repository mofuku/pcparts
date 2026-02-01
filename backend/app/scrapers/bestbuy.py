"""
Best Buy Products API adapter.

Official API documentation: https://bestbuyapis.github.io/api-documentation/
"""

import asyncio
from decimal import Decimal
from typing import Any, Optional
import httpx


# Map our categories to Best Buy category IDs
CATEGORY_MAP = {
    "cpu": "abcat0507002",           # CPUs / Processors
    "gpu": "abcat0507002",           # Graphics Cards (note: may need refinement)
    "motherboard": "abcat0507006",   # Motherboards
    "ram": "abcat0503002",           # Computer Memory
    "storage": "pcmcat158900050001", # Solid State Drives
    "psu": "abcat0507009",           # Power Supplies
    "case": "abcat0507008",          # Computer Cases
    "cooler": "abcat0507005",        # CPU Cooling
}

# Map Best Buy spec names to our normalized keys
SPEC_MAP = {
    "Number of Cores": "cores",
    "Processor Speed": "base_clock",
    "Socket Type": "socket",
    "Memory Type": "memory_type",
    "Memory Speed": "speed",
    "Total Memory Capacity": "capacity",
    "Graphics Memory": "vram",
    "Form Factor": "form_factor",
    "Wattage": "wattage",
    "Chipset Brand": "chipset",
}


class BestBuyAdapter:
    """
    Adapter for Best Buy's Products API.
    
    Usage:
        adapter = BestBuyAdapter(api_key="YOUR_KEY")
        products = await adapter.fetch_category("cpu")
    """
    
    BASE_URL = "https://api.bestbuy.com/v1"
    
    def __init__(
        self,
        api_key: str,
        requests_per_second: int = 5,
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.requests_per_second = requests_per_second
        self.timeout = timeout
        self._last_request_time = 0.0
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client
    
    async def _make_request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make a rate-limited request to the API."""
        # Rate limiting
        now = asyncio.get_event_loop().time()
        min_interval = 1.0 / self.requests_per_second
        elapsed = now - self._last_request_time
        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)
        
        client = await self._get_client()
        
        # Add API key
        params = params or {}
        params["apiKey"] = self.api_key
        params["format"] = "json"
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            self._last_request_time = asyncio.get_event_loop().time()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                # Rate limited - wait and retry
                await asyncio.sleep(5)
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            raise
    
    def get_category_id(self, category: str) -> str:
        """Get Best Buy category ID from our category name."""
        return CATEGORY_MAP.get(category, category)
    
    def _parse_product(self, raw: dict) -> dict:
        """Parse a raw Best Buy product into our format."""
        # Extract specs from details array
        specs = {}
        for detail in raw.get("details", []):
            name = detail.get("name", "")
            value = detail.get("value", "")
            
            # Map to our normalized keys
            if name in SPEC_MAP:
                # Clean up values (remove units like "gigahertz")
                clean_value = value.split()[0] if value else ""
                specs[SPEC_MAP[name]] = clean_value
        
        # Determine stock status
        in_stock = raw.get("onlineAvailability", False) or raw.get("inStoreAvailability", False)
        
        return {
            "sku": str(raw.get("sku", "")),
            "name": raw.get("name", ""),
            "manufacturer": raw.get("manufacturer", ""),
            "price": Decimal(str(raw.get("salePrice", 0))),
            "regular_price": Decimal(str(raw.get("regularPrice", 0))),
            "on_sale": raw.get("onSale", False),
            "url": raw.get("url", ""),
            "in_stock": in_stock,
            "specs": specs,
            "category_path": [c.get("name") for c in raw.get("categoryPath", [])],
        }
    
    async def fetch_category(
        self,
        category: str,
        page_size: int = 100,
        max_pages: int = 10,
    ) -> list[dict]:
        """
        Fetch all products in a category.
        
        Args:
            category: Our category name (cpu, gpu, etc.)
            page_size: Products per page (max 100)
            max_pages: Maximum pages to fetch
        
        Returns:
            List of parsed products
        """
        category_id = self.get_category_id(category)
        products = []
        page = 1
        
        while page <= max_pages:
            # Build query
            endpoint = f"products(categoryPath.id={category_id})"
            params = {
                "show": "sku,name,manufacturer,salePrice,regularPrice,onSale,url,categoryPath,details,inStoreAvailability,onlineAvailability",
                "pageSize": min(page_size, 100),
                "page": page,
            }
            
            data = await self._make_request(endpoint, params)
            
            raw_products = data.get("products", [])
            if not raw_products:
                break
            
            for raw in raw_products:
                products.append(self._parse_product(raw))
            
            # Check if there are more pages
            total = data.get("total", 0)
            fetched = data.get("to", 0)
            if fetched >= total:
                break
            
            page += 1
        
        return products
    
    async def search(self, query: str, limit: int = 20) -> list[dict]:
        """
        Search for products by keyword.
        
        Args:
            query: Search terms
            limit: Max results to return
        
        Returns:
            List of parsed products
        """
        # URL-encode and build search endpoint
        endpoint = f"products(search={query})"
        params = {
            "show": "sku,name,manufacturer,salePrice,regularPrice,onSale,url,categoryPath,details,inStoreAvailability,onlineAvailability",
            "pageSize": min(limit, 100),
        }
        
        data = await self._make_request(endpoint, params)
        
        return [self._parse_product(raw) for raw in data.get("products", [])]
    
    async def get_product(self, sku: str) -> Optional[dict]:
        """
        Get a specific product by SKU.
        
        Args:
            sku: Best Buy SKU
        
        Returns:
            Parsed product or None if not found
        """
        endpoint = f"products(sku={sku})"
        params = {
            "show": "sku,name,manufacturer,salePrice,regularPrice,onSale,url,categoryPath,details,inStoreAvailability,onlineAvailability",
        }
        
        data = await self._make_request(endpoint, params)
        
        products = data.get("products", [])
        if not products:
            return None
        
        return self._parse_product(products[0])
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
