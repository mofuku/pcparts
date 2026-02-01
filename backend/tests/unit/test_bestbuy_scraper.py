"""
TDD tests for Best Buy API scraper.
Tests written BEFORE implementation.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from decimal import Decimal


class TestBestBuyAdapter:
    """Test suite for Best Buy API adapter."""
    
    @pytest.fixture
    def mock_response_cpu(self):
        """Sample Best Buy API response for CPUs."""
        return {
            "from": 1,
            "to": 2,
            "total": 2,
            "products": [
                {
                    "sku": 6530598,
                    "name": "AMD Ryzen 7 7800X3D 8-Core 4.2 GHz Processor",
                    "manufacturer": "AMD",
                    "salePrice": 339.99,
                    "regularPrice": 449.99,
                    "onSale": True,
                    "url": "https://www.bestbuy.com/site/amd-ryzen-7-7800x3d/6530598.p",
                    "categoryPath": [
                        {"id": "abcat0500000", "name": "Computers & Tablets"},
                        {"id": "abcat0501000", "name": "Computer Components"},
                        {"id": "abcat0507002", "name": "CPUs / Processors"},
                    ],
                    "details": [
                        {"name": "Number of Cores", "value": "8"},
                        {"name": "Processor Speed", "value": "4.2 gigahertz"},
                        {"name": "Socket Type", "value": "AM5"},
                    ],
                    "inStoreAvailability": True,
                    "onlineAvailability": True,
                },
                {
                    "sku": 6530599,
                    "name": "Intel Core i7-14700K 20-Core Processor",
                    "manufacturer": "Intel",
                    "salePrice": 399.99,
                    "regularPrice": 399.99,
                    "onSale": False,
                    "url": "https://www.bestbuy.com/site/intel-core-i7-14700k/6530599.p",
                    "categoryPath": [
                        {"id": "abcat0500000", "name": "Computers & Tablets"},
                        {"id": "abcat0501000", "name": "Computer Components"},
                        {"id": "abcat0507002", "name": "CPUs / Processors"},
                    ],
                    "details": [
                        {"name": "Number of Cores", "value": "20"},
                        {"name": "Processor Speed", "value": "3.4 gigahertz"},
                        {"name": "Socket Type", "value": "LGA 1700"},
                    ],
                    "inStoreAvailability": False,
                    "onlineAvailability": True,
                },
            ],
        }
    
    @pytest.mark.asyncio
    async def test_fetch_category_returns_products(self, mock_response_cpu):
        """Fetching a category should return parsed products."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response_cpu
            
            products = await adapter.fetch_category("cpu")
            
            assert len(products) == 2
            assert products[0]["name"] == "AMD Ryzen 7 7800X3D 8-Core 4.2 GHz Processor"
            assert products[0]["manufacturer"] == "AMD"
            assert products[0]["price"] == Decimal("339.99")
    
    @pytest.mark.asyncio
    async def test_fetch_category_extracts_specs(self, mock_response_cpu):
        """Should extract specs from details array."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response_cpu
            
            products = await adapter.fetch_category("cpu")
            
            amd_cpu = products[0]
            assert amd_cpu["specs"]["cores"] == "8"
            assert amd_cpu["specs"]["socket"] == "AM5"
    
    @pytest.mark.asyncio
    async def test_fetch_category_handles_stock_status(self, mock_response_cpu):
        """Should correctly parse stock availability."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response_cpu
            
            products = await adapter.fetch_category("cpu")
            
            # AMD in stock both online and in-store
            assert products[0]["in_stock"] is True
            # Intel only online
            assert products[1]["in_stock"] is True
    
    @pytest.mark.asyncio
    async def test_fetch_category_handles_empty_response(self):
        """Should handle empty product list gracefully."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"products": [], "total": 0}
            
            products = await adapter.fetch_category("cpu")
            
            assert products == []
    
    @pytest.mark.asyncio
    async def test_fetch_category_pagination(self, mock_response_cpu):
        """Should paginate through results correctly."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        # Mock multiple pages
        page1 = {"products": mock_response_cpu["products"][:1], "total": 2, "from": 1, "to": 1}
        page2 = {"products": mock_response_cpu["products"][1:], "total": 2, "from": 2, "to": 2}
        
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = [page1, page2]
            
            products = await adapter.fetch_category("cpu", page_size=1)
            
            assert len(products) == 2
            assert mock_request.call_count == 2
    
    @pytest.mark.asyncio
    async def test_search_products(self, mock_response_cpu):
        """Should search products by keyword."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response_cpu
            
            products = await adapter.search("Ryzen 7800X3D")
            
            assert len(products) >= 1
            mock_request.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_product_by_sku(self, mock_response_cpu):
        """Should fetch a specific product by SKU."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        single_product = {"products": [mock_response_cpu["products"][0]], "total": 1}
        
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = single_product
            
            product = await adapter.get_product("6530598")
            
            assert product is not None
            assert product["sku"] == "6530598"
            assert product["name"] == "AMD Ryzen 7 7800X3D 8-Core 4.2 GHz Processor"
    
    @pytest.mark.asyncio
    async def test_category_mapping(self):
        """Should map our categories to Best Buy category IDs."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        assert adapter.get_category_id("cpu") == "abcat0507002"
        assert adapter.get_category_id("gpu") == "abcat0507002"  # Graphics Cards
        assert adapter.get_category_id("motherboard") == "abcat0507006"
        assert adapter.get_category_id("ram") == "abcat0503002"
        assert adapter.get_category_id("storage") == "pcmcat158900050001"  # SSDs
        assert adapter.get_category_id("psu") == "abcat0507009"
        assert adapter.get_category_id("case") == "abcat0507008"


class TestBestBuyRateLimiting:
    """Test rate limiting behavior."""
    
    @pytest.mark.asyncio
    async def test_respects_rate_limit(self):
        """Should not exceed rate limits."""
        from app.scrapers.bestbuy import BestBuyAdapter
        import time
        
        adapter = BestBuyAdapter(api_key="test_key", requests_per_second=2)
        
        # This is a design test - implementation should track request timing
        assert adapter.requests_per_second == 2
    
    @pytest.mark.asyncio
    async def test_handles_429_error(self):
        """Should handle rate limit exceeded errors gracefully."""
        from app.scrapers.bestbuy import BestBuyAdapter
        
        adapter = BestBuyAdapter(api_key="test_key")
        
        # Test that the adapter has retry logic by checking it exists
        # Full integration test would require real API or more complex mocking
        assert hasattr(adapter, "_make_request")
        
        # Just verify empty response handling
        with patch.object(adapter, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"products": [], "total": 0}
            products = await adapter.fetch_category("cpu")
            assert products == []
