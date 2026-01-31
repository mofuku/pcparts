# PCParts — Find the best parts at the best price

## The Problem
Building a PC is fragmented:
- PCPartPicker is useful but US-centric, cluttered, affiliate-driven
- Price comparison requires 10+ tabs
- Compatibility checking is manual guesswork
- No easy way to optimize price/performance ratio

## The Solution
One place to:
1. **Aggregate prices** across all major retailers (regional)
2. **Check compatibility** automatically
3. **Optimize builds** for budget/performance targets
4. **Track prices** and alert on deals

## MVP Scope
- [ ] Price scraping from 5+ retailers
- [ ] Basic compatibility rules (socket, RAM, PSU wattage)
- [ ] Build list with total price
- [ ] Price history graphs
- [ ] Simple web UI

## Differentiators
- Clean, fast, no bloat
- Regional focus (start with one market, do it well)
- Performance/$ scoring
- AI-assisted build recommendations

## Tech Stack (TBD by team)
- Backend: Python (FastAPI) or Node
- Scraping: Playwright/Puppeteer
- Data: SQLite → Postgres
- Frontend: React or Svelte
- Hosting: Vercel/Railway

## Team
- **PM Agent**: Product decisions, priorities, user stories
- **Backend Agent**: API, scrapers, data pipeline
- **Frontend Agent**: UI/UX, web app
- **Data Agent**: Retailer research, price sources, compatibility DB

---
*Built by Milos & crew*
