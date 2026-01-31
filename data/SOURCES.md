# PC Parts Price Aggregator - Data Sources

*Research completed: January 31, 2026*

This document catalogs all viable data sources for PC part prices, specifications, and related data for the PCParts aggregator project.

---

## Table of Contents
1. [Retail APIs (Official)](#retail-apis-official)
2. [Retail Sources (Scraping Required)](#retail-sources-scraping-required)
3. [Existing Datasets](#existing-datasets)
4. [Benchmark Databases](#benchmark-databases)
5. [Specs & Compatibility Databases](#specs--compatibility-databases)
6. [Recommendations & Strategy](#recommendations--strategy)

---

## Retail APIs (Official)

### ⭐ Best Buy Products API
**RECOMMENDED - Best official API for PC parts**

| Attribute | Details |
|-----------|---------|
| **URL** | https://developer.bestbuy.com/ |
| **Documentation** | https://bestbuyapis.github.io/api-documentation/ |
| **API Type** | REST API (JSON/XML) |
| **API Availability** | ✅ Official, Free API key |
| **Coverage** | 725,000+ products, 100+ brands |
| **Data Quality** | Excellent - SKU, name, salePrice, specs, categories, stock |
| **Scraping Difficulty** | N/A (Official API) |
| **Update Frequency** | Real-time |
| **Rate Limits** | Yes (check current limits) |

**Key Features:**
- Products API: Search by category, filter by attributes
- Stores API: Inventory by location
- Categories API: Full taxonomy
- Recommendations API: Related products
- Cursor pagination for large result sets (100 items/page max)
- Filter by: manufacturer, price range, category, condition
- Sort by: price, bestsellers, customerReviewAverage

**Example Query:**
```
GET /v1/products(categoryPath.name="Computer Components")?format=json&show=sku,name,salePrice&apiKey=YOUR_KEY
```

**Verdict:** 🟢 Start here. Robust, well-documented, reliable.

---

### Amazon Product Advertising API (PA-API 5.0)

| Attribute | Details |
|-----------|---------|
| **URL** | https://webservices.amazon.com/paapi5/documentation/ |
| **API Type** | REST API (JSON) |
| **API Availability** | ✅ Official (requires Associates account) |
| **Coverage** | Millions of products |
| **Data Quality** | Good - prices, specs, images, reviews |
| **Scraping Difficulty** | N/A (Official API) |
| **Update Frequency** | Real-time |
| **Rate Limits** | Based on sales performance |

**Requirements:**
- Must be an Amazon Associate
- Rate limits tied to affiliate sales (starts very low)
- Need to generate sales to maintain access

**Key Operations:**
- SearchItems: Search by keywords, categories
- GetItems: Retrieve product details by ASIN
- GetBrowseNodes: Category navigation

**Verdict:** 🟡 Good data but restrictive. Rate limits are tied to affiliate sales. Not ideal for starting out.

---

### eBay Browse API

| Attribute | Details |
|-----------|---------|
| **URL** | https://developer.ebay.com/api-docs/buy/browse/overview.html |
| **API Type** | REST API (JSON) |
| **API Availability** | ✅ Official (requires developer account) |
| **Coverage** | New and used PC parts, auctions |
| **Data Quality** | Variable - condition varies, good for used market |
| **Scraping Difficulty** | N/A (Official API) |
| **Update Frequency** | Real-time |

**Key Features:**
- Search by keyword, category, image, GTIN
- Filter by condition, price, location, seller
- Compatibility checking for parts
- Refinements/facets for filtering UI

**Limitations:**
- Returns FIXED_PRICE items by default
- Max 10,000 items per result set
- Production access requires approval

**Verdict:** 🟡 Good for used market and price comparison. Useful secondary source.

---

### Newegg Marketplace API (SDK)

| Attribute | Details |
|-----------|---------|
| **URL** | https://developer.newegg.com/ |
| **API Type** | Marketplace SDK (.NET, Java) |
| **API Availability** | ⚠️ For sellers only |
| **Coverage** | N/A for consumers |
| **Scraping Difficulty** | Hard (Cloudflare protection) |

**Reality Check:**
The Newegg Developer Portal is for **Marketplace sellers**, not for accessing product data. There is no official consumer-facing product API.

**Alternative:** Web scraping (see below)

**Verdict:** 🔴 No public product API. Must scrape.

---

### Walmart Developer API

| Attribute | Details |
|-----------|---------|
| **URL** | https://developer.walmart.com/ |
| **API Type** | REST API |
| **API Availability** | ⚠️ For sellers/partners only |
| **Coverage** | Various including electronics |

**Reality Check:**
Like Newegg, Walmart's APIs are for:
- Marketplace sellers
- 1P suppliers
- Advertising partners
- Transportation carriers

No public product search API for aggregators.

**Verdict:** 🔴 No public product API for price aggregation.

---

## Retail Sources (Scraping Required)

### Newegg

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.newegg.com |
| **Coverage** | Largest PC parts specialty retailer |
| **Scraping Difficulty** | 🔴 Hard |
| **Anti-bot Measures** | Cloudflare, rate limiting, CAPTCHAs |
| **Data Quality** | Excellent specs, prices, reviews, stock |
| **Update Frequency** | Daily pricing changes |

**Scraping Approach:**
- Residential proxies required
- Browser automation (Playwright/Puppeteer)
- Rate limiting: ~1 request/5 seconds
- VPN rotation recommended

---

### PCPartPicker

| Attribute | Details |
|-----------|---------|
| **URL** | https://pcpartpicker.com |
| **Coverage** | Aggregated prices from multiple retailers |
| **Scraping Difficulty** | 🔴 Hard/Blocked |
| **Anti-bot Measures** | Cloudflare, aggressive blocking |
| **Data Quality** | Excellent - specs, compatibility, multi-retailer prices |

**⚠️ CRITICAL WARNING:**
From their `robots.txt`:
```
Content-Signal: search=yes, ai-train=no, ai-input=no
Disallow: /api/
User-agent: ClaudeBot
Disallow: /
```

PCPartPicker explicitly:
- Blocks AI scraping/training
- Blocks their API
- Blocks Claude and GPT bots
- Uses aggressive Cloudflare protection
- 60-second crawl delay

**Legal Considerations:**
Scraping PCPartPicker likely violates their ToS and may expose you to legal risk. They are actively protecting their data.

**Alternative:** Use the **docyx/pc-part-dataset** (see Datasets section)

**Verdict:** 🔴 Do not scrape. Use existing dataset or build your own from retailers.

---

### Micro Center

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.microcenter.com |
| **Coverage** | Excellent for CPUs/GPUs (often best in-store prices) |
| **Scraping Difficulty** | 🔴 Hard |
| **Anti-bot Measures** | Cloudflare protection |
| **Data Quality** | Good - local inventory, in-store deals |

**Note:** Often has exclusive in-store deals not available online.

---

### B&H Photo Video

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.bhphotovideo.com |
| **Coverage** | Good PC parts selection, strong GPU/monitor inventory |
| **Scraping Difficulty** | 🔴 Hard |
| **Anti-bot Measures** | Cloudflare (403 responses) |
| **Data Quality** | Excellent specs and descriptions |

---

## Existing Datasets

### ⭐ docyx/pc-part-dataset (GitHub)
**RECOMMENDED - Best open dataset**

| Attribute | Details |
|-----------|---------|
| **URL** | https://github.com/docyx/pc-part-dataset |
| **Part Count** | 66,778 parts |
| **Last Updated** | July 23, 2025 |
| **Formats** | JSON, JSON Lines, CSV |
| **License** | MIT |

**Categories Covered:**
- CPUs
- CPU Coolers
- Motherboards
- Memory (RAM)
- Storage
- Video Cards (GPUs)
- Cases
- Power Supplies
- Optical Drives
- Operating Systems
- Monitors
- External Storage
- Case Accessories
- Case Fans
- Fan Controllers
- Thermal Compound
- UPS Systems
- Sound Cards
- Network Adapters
- Headphones
- Keyboards
- Mice
- Speakers
- Webcams

**Data Fields (varies by category):**
- Name, manufacturer
- Price (at time of scrape)
- Specs (cores, clock speed, TDP, socket, etc.)
- Ratings/reviews

**Usage:**
```bash
git clone https://github.com/docyx/pc-part-dataset
# Data in ./data directory
```

**Limitations:**
- Static dataset (not real-time prices)
- Prices become stale
- Scraped from PCPartPicker (ethical gray area for reuse?)

**Verdict:** 🟢 Excellent for specs database. Use Best Buy API for live prices.

---

## Benchmark Databases

### PassMark

| Attribute | Details |
|-----------|---------|
| **CPU Benchmarks** | https://www.cpubenchmark.net/cpu-list/ |
| **GPU Benchmarks** | https://www.videocardbenchmark.net/gpu_list.php |
| **Data Available** | Benchmark scores, rankings, value scores, prices |
| **API Availability** | ❌ No official API |
| **Scraping Difficulty** | 🟡 Medium |

**Data Fields:**
- Processor/GPU name
- PassMark score
- Rank
- Price (where available)
- Value score (performance per dollar)

**Coverage:**
- Thousands of CPUs and GPUs
- Historical benchmark data
- Price tracking

**Verdict:** 🟡 Valuable for performance comparisons. No API - requires scraping.

---

### UserBenchmark

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.userbenchmark.com |
| **API Availability** | ❌ No public API |
| **Scraping Difficulty** | 🟡 Medium |
| **Controversy** | Known for biased benchmark methodology |

**Verdict:** 🟠 Controversial methodology. Consider PassMark or 3DMark instead.

---

### 3DMark

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.3dmark.com |
| **Data Available** | GPU/CPU benchmark scores (50M+ results) |
| **API Availability** | ❌ No public API |
| **Scraping Difficulty** | 🟡 Medium |

**Verdict:** 🟡 Good benchmark data, no API access.

---

### TechPowerUp GPU Database

| Attribute | Details |
|-----------|---------|
| **URL** | https://www.techpowerup.com/gpu-specs/ |
| **Coverage** | Comprehensive GPU specs database |
| **API Availability** | ❌ No official API |
| **Scraping Difficulty** | 🔴 Hard (bot detection) |

**Data Available:**
- GPU specifications
- Clock speeds
- Memory configuration
- TDP
- Launch dates

**Verdict:** 🟡 Excellent specs data, aggressive bot protection.

---

## Specs & Compatibility Databases

### CPU Socket Compatibility

No single authoritative API. Must build from:
1. Manufacturer specs (Intel ARK, AMD specs)
2. Motherboard manufacturer listings
3. pc-part-dataset (socket information included)

### RAM Compatibility

Factors:
- DDR generation (DDR4 vs DDR5)
- Speed ratings (3200MHz, etc.)
- Motherboard QVL lists

**Data Sources:**
- Motherboard manufacturer QVL (Qualified Vendor Lists)
- Crucial Memory Advisor (https://www.crucial.com/store/advisor)

### GPU Compatibility

Factors:
- PCIe slot generation
- Physical size (length, slots)
- Power requirements (TDP, connectors)
- Case clearance

---

## Recommendations & Strategy

### Recommended Data Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PCParts Data Pipeline                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SPECS DATABASE (Static, update monthly)                    │
│  ├── docyx/pc-part-dataset (66k parts)                      │
│  ├── PassMark benchmarks (scraped)                          │
│  └── TechPowerUp specs (scraped if possible)                │
│                                                              │
│  LIVE PRICES (Real-time/hourly)                             │
│  ├── Best Buy API ⭐ (Primary - 725k products)               │
│  ├── eBay Browse API (Used/auction market)                  │
│  └── Amazon PA-API (If affiliate sales support it)          │
│                                                              │
│  SUPPLEMENTARY (Weekly scrape with care)                    │
│  ├── Newegg (high-value scraping target)                    │
│  └── B&H Photo (secondary)                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: MVP (Week 1-2)
1. **Best Buy API** - Get API key, build integration
2. **docyx/pc-part-dataset** - Import for specs database
3. **Match products** - Link Best Buy SKUs to part database

### Phase 2: Expansion (Week 3-4)
1. **eBay Browse API** - Add used market pricing
2. **PassMark scraping** - Add benchmark scores
3. **Build compatibility rules** - Socket, RAM, PCIe matching

### Phase 3: Advanced (Month 2+)
1. **Newegg scraper** - Careful implementation with proxies
2. **Amazon PA-API** - If affiliate sales justify access
3. **Price history tracking** - Store historical data
4. **Alert system** - Price drop notifications

### Key Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| API rate limits | Implement caching, queue requests |
| Scraping blocks | Residential proxies, rate limiting |
| Legal issues | Avoid PCPartPicker, respect robots.txt |
| Stale data | Real-time API for prices, periodic spec updates |
| Data matching | Build robust SKU/UPC matching system |

### Cost Estimates

| Service | Cost |
|---------|------|
| Best Buy API | Free |
| eBay API | Free (with limits) |
| Amazon PA-API | Free (but requires affiliate sales) |
| Residential Proxies | ~$50-200/month for scraping |
| Infrastructure | ~$20-100/month (servers, storage) |

---

## Appendix: Quick Reference

### Best Sources by Use Case

| Use Case | Recommended Source |
|----------|-------------------|
| Live prices | Best Buy API |
| Complete specs | docyx/pc-part-dataset |
| Used/refurbished | eBay Browse API |
| Benchmark data | PassMark (scrape) |
| GPU specs | TechPowerUp (scrape) |
| Price history | Build your own from API data |

### Scraping Tools

- **Scrapy** - Python framework (https://scrapy.org)
- **Playwright** - Browser automation (better for JS sites)
- **Puppeteer** - Chrome automation
- **Selenium** - Older but stable

### Anti-Detection

- Residential proxy services (BrightData, Oxylabs)
- Browser fingerprint rotation
- Request timing randomization
- User-agent rotation

---

*Last updated: January 31, 2026*
*Author: PCParts Data Research Agent*
