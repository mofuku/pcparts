# PCParts — System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│                   (Svelte + Tailwind)                        │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────────┐
│                      API Server                              │
│                      (FastAPI)                               │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   /search    │   /parts     │   /builds    │   /prices      │
└──────────────┴──────────────┴──────────────┴────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Data Layer                              │
│                     (SQLite/Postgres)                        │
├──────────────┬──────────────┬──────────────┬────────────────┤
│    Parts     │    Prices    │   Retailers  │    Builds      │
└──────────────┴──────────────┴──────────────┴────────────────┘
                          ▲
┌─────────────────────────┴───────────────────────────────────┐
│                    Scraper Workers                           │
│              (Async, Queue-based, Per-retailer)              │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. API Server (FastAPI)

**Why FastAPI:**
- Async native (good for I/O-bound price fetching)
- Auto-generated OpenAPI docs
- Type hints = fewer bugs
- Fast enough for MVP

**Endpoints:**

```
GET  /api/v1/parts                    # List/search parts
GET  /api/v1/parts/{id}               # Part detail
GET  /api/v1/parts/{id}/prices        # Prices for a part
GET  /api/v1/parts/{id}/history       # Price history

GET  /api/v1/categories               # CPU, GPU, RAM, etc.
GET  /api/v1/retailers                # List retailers

POST /api/v1/builds                   # Create a build
GET  /api/v1/builds/{id}              # Get build
PUT  /api/v1/builds/{id}              # Update build
GET  /api/v1/builds/{id}/compatibility # Check compatibility

GET  /api/v1/search?q=                # Full-text search
```

### 2. Data Model

```python
# Core entities

class Category(Enum):
    CPU = "cpu"
    GPU = "gpu"
    MOTHERBOARD = "motherboard"
    RAM = "ram"
    STORAGE = "storage"
    PSU = "psu"
    CASE = "case"
    COOLER = "cooler"

class Part:
    id: str                    # Unique identifier
    name: str                  # "AMD Ryzen 9 7950X"
    brand: str                 # "AMD"
    category: Category
    specs: dict                # Category-specific specs
    created_at: datetime
    updated_at: datetime

class Retailer:
    id: str                    # "newegg", "amazon", etc.
    name: str                  # "Newegg"
    url: str                   # Base URL
    active: bool

class Price:
    id: str
    part_id: str
    retailer_id: str
    price: Decimal             # Current price
    currency: str              # "USD"
    url: str                   # Direct link to product
    in_stock: bool
    scraped_at: datetime

class PriceHistory:
    part_id: str
    retailer_id: str
    price: Decimal
    recorded_at: datetime

class Build:
    id: str
    name: str
    parts: list[str]           # Part IDs
    created_at: datetime
    updated_at: datetime
```

### 3. Category-Specific Specs

```python
# CPU specs
cpu_specs = {
    "socket": "AM5",
    "cores": 16,
    "threads": 32,
    "base_clock": 4.5,        # GHz
    "boost_clock": 5.7,       # GHz
    "tdp": 170,               # Watts
    "memory_type": "DDR5",
}

# Motherboard specs
motherboard_specs = {
    "socket": "AM5",
    "chipset": "X670E",
    "form_factor": "ATX",
    "memory_type": "DDR5",
    "memory_slots": 4,
    "max_memory": 128,        # GB
    "pcie_slots": {"x16": 2, "x4": 1, "x1": 2},
    "m2_slots": 4,
}

# RAM specs
ram_specs = {
    "type": "DDR5",
    "capacity": 32,           # GB
    "speed": 6000,            # MHz
    "modules": 2,
    "cas_latency": 30,
}

# GPU specs
gpu_specs = {
    "chipset": "RTX 4090",
    "vram": 24,               # GB
    "tdp": 450,               # Watts
    "length": 336,            # mm
    "slots": 3,
}

# PSU specs
psu_specs = {
    "wattage": 850,
    "efficiency": "80+ Gold",
    "modular": "full",
    "form_factor": "ATX",
}
```

### 4. Compatibility Engine

**Rules to implement (MVP):**

| Rule | Check |
|------|-------|
| CPU-Motherboard | socket match |
| RAM-Motherboard | DDR type match |
| RAM-CPU | DDR type match |
| GPU-Case | length fits |
| PSU-Build | wattage >= total TDP * 1.2 |
| Cooler-Case | height fits |
| Cooler-CPU | socket compatible |

```python
class CompatibilityChecker:
    def check(self, build: Build) -> list[CompatibilityIssue]:
        issues = []
        
        cpu = self.get_part(build, Category.CPU)
        mobo = self.get_part(build, Category.MOTHERBOARD)
        ram = self.get_part(build, Category.RAM)
        gpu = self.get_part(build, Category.GPU)
        psu = self.get_part(build, Category.PSU)
        
        # CPU-Motherboard socket
        if cpu and mobo:
            if cpu.specs["socket"] != mobo.specs["socket"]:
                issues.append(CompatibilityIssue(
                    severity="error",
                    message=f"CPU socket {cpu.specs['socket']} != motherboard {mobo.specs['socket']}"
                ))
        
        # RAM-Motherboard type
        if ram and mobo:
            if ram.specs["type"] != mobo.specs["memory_type"]:
                issues.append(CompatibilityIssue(
                    severity="error",
                    message=f"RAM type {ram.specs['type']} != motherboard {mobo.specs['memory_type']}"
                ))
        
        # PSU wattage
        if psu:
            total_tdp = sum(
                p.specs.get("tdp", 0) 
                for p in build.parts 
                if "tdp" in p.specs
            )
            if psu.specs["wattage"] < total_tdp * 1.2:
                issues.append(CompatibilityIssue(
                    severity="warning",
                    message=f"PSU {psu.specs['wattage']}W may be insufficient for {total_tdp}W TDP"
                ))
        
        return issues
```

### 5. Scraper Architecture

```
┌────────────────────────────────────────────┐
│              Scheduler (cron)               │
│         "scrape newegg every 6h"            │
└─────────────────────┬──────────────────────┘
                      ▼
┌────────────────────────────────────────────┐
│              Task Queue (Redis/SQLite)      │
│    [{retailer: newegg, category: cpu}, ...] │
└─────────────────────┬──────────────────────┘
                      ▼
┌────────────────────────────────────────────┐
│              Worker Pool (async)            │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│   │ Worker  │ │ Worker  │ │ Worker  │      │
│   └─────────┘ └─────────┘ └─────────┘      │
└─────────────────────┬──────────────────────┘
                      ▼
┌────────────────────────────────────────────┐
│          Retailer Adapters                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ Newegg   │ │ Amazon   │ │ BestBuy  │    │
│  │ Adapter  │ │ Adapter  │ │ Adapter  │    │
│  └──────────┘ └──────────┘ └──────────┘    │
└─────────────────────┬──────────────────────┘
                      ▼
┌────────────────────────────────────────────┐
│              Database                       │
│         (upsert prices, history)            │
└────────────────────────────────────────────┘
```

**Adapter Interface:**

```python
class RetailerAdapter(ABC):
    @abstractmethod
    async def search(self, query: str) -> list[ScrapedPart]:
        pass
    
    @abstractmethod
    async def get_price(self, product_url: str) -> ScrapedPrice:
        pass
    
    @abstractmethod
    async def list_category(self, category: Category) -> list[ScrapedPart]:
        pass
```

### 6. Frontend (Svelte + Tailwind)

**Why Svelte:**
- Smaller bundle (fast load)
- Less boilerplate than React
- Reactivity built-in
- Good for MVP speed

**Pages:**

| Route | Description |
|-------|-------------|
| `/` | Home + search |
| `/parts` | Browse by category |
| `/parts/:id` | Part detail + prices |
| `/build` | Build configurator |
| `/build/:id` | Saved build |

**Components:**

```
components/
├── PartCard.svelte       # Part thumbnail
├── PriceTable.svelte     # Retailer prices
├── PriceChart.svelte     # History graph
├── BuildList.svelte      # Parts in build
├── CompatCheck.svelte    # Compatibility warnings
├── SearchBar.svelte      # Autocomplete search
└── ui/                   # Base components
    ├── Button.svelte
    ├── Card.svelte
    ├── Input.svelte
    └── Badge.svelte
```

## Tech Stack Summary

| Layer | Tech | Rationale |
|-------|------|-----------|
| Frontend | Svelte + Tailwind | Fast, minimal, easy |
| API | FastAPI | Async, typed, documented |
| Database | SQLite → Postgres | Simple start, scale later |
| Scraping | Playwright | Handles JS-heavy sites |
| Queue | SQLite (MVP) → Redis | Keep it simple |
| Hosting | Railway/Fly.io | Easy deploy, cheap |

## Directory Structure

```
pcparts/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   ├── config.py         # Settings
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── api/              # Route handlers
│   │   ├── services/         # Business logic
│   │   ├── scrapers/         # Retailer adapters
│   │   └── compatibility/    # Compat engine
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── alembic/              # Migrations
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── routes/
│   │   ├── lib/
│   │   └── app.html
│   ├── static/
│   ├── tests/
│   └── package.json
└── docs/
    ├── ARCHITECTURE.md
    ├── API.md
    └── PRD.md
```

---

*Architecture by Milos • 2026-01-31*
