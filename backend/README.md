# PCParts Backend

Price aggregation API for PC components.

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev,scraping]"

# Seed the database
python -m scripts.seed

# Run the server
python -m app.main
# or
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes
│   │   ├── parts.py   # Parts & categories
│   │   ├── prices.py  # Prices & retailers
│   │   └── builds.py  # Build lists
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── scrapers/      # Scraper framework
│   │   ├── base.py    # BaseScraper class
│   │   ├── manager.py # Orchestration
│   │   └── example.py # Template scraper
│   ├── config.py      # Settings
│   ├── database.py    # DB connection
│   └── main.py        # FastAPI app
├── scripts/
│   └── seed.py        # Database seeding
└── pyproject.toml     # Dependencies
```

## API Endpoints

### Parts
- `GET /parts` - List parts (filter by category, manufacturer, search)
- `GET /parts/{id}` - Get part with prices
- `POST /parts` - Create part
- `GET /parts/categories` - List categories

### Prices
- `GET /prices/retailers` - List retailers
- `POST /prices` - Record price (scraper use)
- `GET /prices/history/{part_id}` - Price history
- `GET /prices/compare/{part_id}` - Compare across retailers

### Builds
- `POST /builds` - Create build
- `GET /builds/{id}` - Get build with items
- `POST /builds/{id}/items` - Add item
- `GET /builds/{id}/compatibility` - Check compatibility

## Adding a New Scraper

1. Copy `app/scrapers/example.py` to `app/scrapers/<retailer>.py`
2. Update retailer info and category mappings
3. Implement `scrape_category()` with actual parsing
4. Register in manager:

```python
manager = ScraperManager(db)
manager.register(YourScraper())
await manager.run_all()
```

## Environment Variables

```bash
PCPARTS_DATABASE_URL=sqlite+aiosqlite:///./pcparts.db
PCPARTS_DEBUG=false
PCPARTS_SCRAPE_INTERVAL_MINUTES=60
PCPARTS_MAX_CONCURRENT_SCRAPERS=5
```
