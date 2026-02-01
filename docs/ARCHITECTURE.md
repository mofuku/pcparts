# PCParts Architecture

Technical architecture document for the PCParts price aggregator.

## Overview

PCParts is a PC component price aggregator that:
1. Scrapes prices from multiple retailers
2. Provides price comparison and history
3. Helps users build compatible PC configurations
4. Tracks deals and price drops

## Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | FastAPI (Python) | Async-native, auto OpenAPI docs, Pydantic validation |
| **Database** | SQLite → PostgreSQL | SQLite for MVP, easy migration path |
| **ORM** | SQLAlchemy 2.0 | Async support, mature ecosystem |
| **Scraping** | httpx + BeautifulSoup/Playwright | httpx for simple pages, Playwright for JS-heavy sites |
| **Frontend** | TBD (React/Svelte) | - |

### Why FastAPI over Express?

1. **Python scraping ecosystem** — BeautifulSoup, Scrapy, Playwright bindings are mature
2. **Async-first** — Built on Starlette, perfect for concurrent scraping
3. **Type safety** — Pydantic models catch errors early, auto-generate OpenAPI
4. **Data science ready** — If we add ML for recommendations, Python is natural fit

---

## Data Model

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CORE ENTITIES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐                   │
│  │ Category │──1:N─│   Part   │──1:N─│ PartSpec │                   │
│  └──────────┘      └──────────┘      └──────────┘                   │
│       │                 │                                            │
│       │                 │                                            │
│       │                 ├────────1:N────────┐                        │
│       │                 │                   │                        │
│       │            ┌────▼────┐        ┌─────▼─────┐                  │
│       │            │  Price  │        │ BuildItem │                  │
│       │            └────┬────┘        └─────┬─────┘                  │
│       │                 │                   │                        │
│       │                 │                   N:1                      │
│       │            N:1  │                   │                        │
│       │                 │              ┌────▼────┐                   │
│       │            ┌────▼────┐         │  Build  │                   │
│       │            │ Retailer│         └─────────┘                   │
│       │            └─────────┘                                       │
│       │                                                              │
│       └──────────────────────┬───────────────────────┐               │
│                              │                       │               │
│                     ┌────────▼────────┐    ┌────────▼────────┐       │
│                     │ CompatRule (A)  │    │ CompatRule (B)  │       │
│                     └─────────────────┘    └─────────────────┘       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Entity Descriptions

#### Category
Part categories (CPU, GPU, RAM, etc.). Used for filtering and compatibility rules.

#### Part
A unique PC component (e.g., "AMD Ryzen 5 7600X"). Deduplicated by manufacturer + model.

#### PartSpec
Flexible key-value specifications. Allows any part type without schema changes.
- CPU: `cores`, `threads`, `socket`, `tdp`
- GPU: `vram`, `memory_type`, `length`, `tdp`
- RAM: `capacity`, `speed`, `type`, `cas_latency`

#### Retailer
A store we scrape from. Tracks scraping status and errors.

#### Price
Price snapshots for history tracking. New row inserted on each scrape.
Query pattern: `ORDER BY scraped_at DESC LIMIT 1` for latest.

#### Build
User-created PC configurations with items, totals, and share tokens.

#### CompatibilityRule
Rules for checking part compatibility. Types:
- `match`: Values must equal (CPU socket = mobo socket)
- `lte/gte`: Numeric comparisons (GPU length ≤ case clearance)
- `in`: Value in list (RAM type in mobo supported types)

---

## API Design

### REST Endpoints

```
/                           GET     API info
/health                     GET     Health check

/parts
  /categories               GET     List categories
  /categories               POST    Create category
  /                         GET     List parts (filter, search, paginate)
  /{id}                     GET     Part with prices
  /                         POST    Create part

/prices
  /retailers                GET     List retailers
  /retailers                POST    Create retailer
  /                         POST    Record price (scraper)
  /history/{part_id}        GET     Price history
  /compare/{part_id}        GET     Compare across retailers

/builds
  /                         GET     List builds
  /                         POST    Create build
  /{id}                     GET     Build with items
  /{id}/items               POST    Add item
  /{id}/items/{item_id}     DELETE  Remove item
  /{id}/compatibility       GET     Check compatibility
  /share/{token}            GET     Get by share token
```

### Response Patterns

**List responses** include pagination:
```json
{
  "items": [...],
  "total": 1234,
  "limit": 50,
  "offset": 0
}
```

**Part with prices** includes latest from each retailer:
```json
{
  "id": 1,
  "full_name": "AMD Ryzen 5 7600X",
  "specs": [{"key": "cores", "value": "6"}],
  "prices": [
    {"retailer": "Amazon", "price": 229.99, "in_stock": true},
    {"retailer": "Newegg", "price": 219.99, "in_stock": true}
  ],
  "lowest_price": 219.99
}
```

---

## Scraper Architecture

### Design Principles

1. **Async-first** — Concurrent scraping with semaphore limits
2. **Extensible** — One file per retailer, common interface
3. **Resilient** — Retries, error tracking, graceful degradation
4. **Observable** — Logging, metrics, status tracking

### Class Hierarchy

```
BaseScraper (abstract)
├── setup() / teardown()    # Resource management
├── scrape_category()       # Main scraping method (abstract)
├── scrape_product()        # Single product update
└── search()                # Product discovery

ScraperManager
├── register(scraper)       # Add scraper
├── run_all(categories)     # Orchestrate all scrapers
├── _run_scraper()          # Run with semaphore
└── _process_scraped_price()# Match and record
```

### Scraper Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        ScraperManager                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Semaphore (5)                         │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │    │
│  │  │ Amazon  │ │ Newegg  │ │  B&H    │ │BestBuy  │ ...   │    │
│  │  │ Scraper │ │ Scraper │ │ Scraper │ │ Scraper │       │    │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘       │    │
│  └───────┼──────────┼──────────┼──────────┼───────────────┘    │
│          │          │          │          │                      │
│          ▼          ▼          ▼          ▼                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   ScrapedPrice Queue                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Part Matcher                          │    │
│  │            (manufacturer + model → Part ID)              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     Database                             │    │
│  │                  (Price table)                           │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Adding a New Retailer

1. Create `app/scrapers/<retailer>.py`
2. Inherit from `BaseScraper`
3. Set retailer info (slug, name, base_url, currency)
4. Implement `scrape_category()` with parsing logic
5. Register in manager

```python
class NewRetailerScraper(BaseScraper):
    retailer_slug = "newretailer-us"
    retailer_name = "New Retailer"
    base_url = "https://newretailer.com"
    currency = "USD"

    async def scrape_category(self, category: str):
        # Fetch pages, parse HTML, yield ScrapedPrice
        async for product in self._paginate(category):
            yield ScrapedPrice(
                manufacturer=product.brand,
                model=product.name,
                price=product.price,
                ...
            )
```

---

## Price History Design

### Storage Strategy

Each scrape creates a new `Price` row (append-only). This enables:
- Full price history without complex updates
- Easy "lowest price ever" queries
- Time-series analysis

### Efficient Queries

**Latest price per retailer:**
```sql
SELECT DISTINCT ON (retailer_id) *
FROM prices
WHERE part_id = ?
ORDER BY retailer_id, scraped_at DESC
```

**Price trend (30 days):**
```sql
SELECT date(scraped_at), MIN(price), AVG(price), MAX(price)
FROM prices
WHERE part_id = ? AND scraped_at > NOW() - INTERVAL '30 days'
GROUP BY date(scraped_at)
```

### Cleanup Strategy (Future)

For long-term storage efficiency:
1. Keep all data for 90 days
2. Aggregate to daily min/max/avg for older data
3. Or use TimescaleDB for automatic compression

---

## Compatibility Checking

### Rule Engine (MVP)

Simple rule evaluation against part specs:

```python
for rule in active_rules:
    spec_a = get_spec(part_a, rule.spec_a)
    spec_b = get_spec(part_b, rule.spec_b)
    
    if rule.type == "match" and spec_a != spec_b:
        issues.append(rule.error_message)
    elif rule.type == "lte" and float(spec_a) > float(spec_b):
        issues.append(rule.error_message)
```

### Future Improvements

1. **DSL for complex rules** — "IF cpu.socket != mobo.socket THEN ERROR"
2. **Inference rules** — "Total TDP = SUM(all parts with TDP)"
3. **ML-based suggestions** — "Users with this CPU often choose..."

---

## Deployment

### MVP (SQLite)

```bash
# Single machine, SQLite file
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Production (PostgreSQL)

```yaml
# docker-compose.yml
services:
  api:
    build: ./backend
    environment:
      PCPARTS_DATABASE_URL: postgresql+asyncpg://...
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:16
    
  redis:
    image: redis:7  # For scraper queue
    
  scraper:
    build: ./backend
    command: python -m scripts.run_scrapers
```

---

## Future Considerations

### Scaling Scrapers

1. **Queue-based** — Redis/RabbitMQ job queue
2. **Distributed** — Multiple scraper workers
3. **Proxy rotation** — Avoid rate limiting

### Price Alerts

1. User creates alert (part_id, target_price)
2. On new price, check if below target
3. Send notification (email, push, webhook)

### AI Features

1. **Build recommendations** — "Best gaming PC under $1500"
2. **Price predictions** — "Price likely to drop next week"
3. **Part matching** — Fuzzy matching scraped products to DB

---

## File Structure

```
pcparts/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── parts.py
│   │   │   ├── prices.py
│   │   │   └── builds.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── parts.py
│   │   │   ├── prices.py
│   │   │   ├── builds.py
│   │   │   └── compatibility.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── parts.py
│   │   │   ├── prices.py
│   │   │   └── builds.py
│   │   ├── scrapers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── manager.py
│   │   │   └── example.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── seed.py
│   ├── pyproject.toml
│   └── README.md
├── frontend/           # TBD
├── docs/
│   └── ARCHITECTURE.md
└── VISION.md
```

---

*Document version: 1.0 | Last updated: Backend scaffold complete*
