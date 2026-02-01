# PCParts

**Find the best parts at the best price for your PC build, in one place.**

![Status](https://img.shields.io/badge/status-alpha-orange)
![Tests](https://img.shields.io/badge/tests-20%20passing-green)

## Quick Start

### Backend

```bash
cd backend
pip install -e ".[dev]"

# Run tests
pytest

# Start server
python -m app.main
# → http://localhost:8000
# → http://localhost:8000/docs (Swagger UI)
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│                   (SvelteKit + Tailwind)                     │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────────┐
│                      API Server                              │
│                      (FastAPI)                               │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   /parts     │   /prices    │   /builds    │   /search      │
└──────────────┴──────────────┴──────────────┴────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Scrapers                                │
│          BestBuyAdapter (official API) + more               │
└─────────────────────────────────────────────────────────────┘
```

## Features

- [x] Price aggregation from Best Buy (official API)
- [x] Compatibility checking (socket, RAM type, PSU wattage)
- [x] Build configurator
- [ ] Price history tracking
- [ ] Deal alerts
- [ ] More retailers (Amazon, Newegg)

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | SvelteKit 2, Tailwind CSS 4 |
| Backend | FastAPI, SQLAlchemy 2, Pydantic 2 |
| Database | SQLite (MVP) → PostgreSQL |
| Scraping | httpx, Best Buy API |
| Testing | pytest, pytest-asyncio |

## Project Structure

```
pcparts/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── scrapers/     # Retailer adapters
│   │   └── services/     # Business logic
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── routes/       # SvelteKit pages
│   │   └── lib/          # Components, utils
│   └── static/
└── docs/
    ├── ARCHITECTURE.md
    ├── API.yaml          # OpenAPI spec
    └── PRD.md
```

## Environment Variables

```bash
# backend/.env
BESTBUY_API_KEY=your_key_here
DATABASE_URL=sqlite:///./pcparts.db
```

Get a Best Buy API key at: https://developer.bestbuy.com/

## Development

### TDD Workflow

```
1. Write failing test
2. Implement minimal code
3. Refactor
4. Commit
```

### Run All Tests

```bash
cd backend && pytest -v
```

### Current Test Coverage

- `test_compatibility.py` — 10 tests (socket, RAM, PSU checks)
- `test_bestbuy_scraper.py` — 10 tests (fetch, search, pagination)

## License

MIT

---

*Built by Milos & crew*
