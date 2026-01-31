# PCParts — Development Lifecycle

## Philosophy
**Test-Driven Development. Small iterations. Ship fast, learn faster.**

---

## Phase 1: Design & Architecture (Current)

### Deliverables
- [ ] **PRD** — What are we building? (PM Agent)
- [ ] **Data Sources** — Where does data come from? (Data Agent)
- [ ] **System Architecture** — How does it all connect? (Backend Agent)
- [ ] **UI/UX Design** — What does the user see? (Frontend Agent)
- [ ] **API Contract** — OpenAPI spec for frontend/backend interface

### Exit Criteria
All docs reviewed and approved. Clear scope for MVP Sprint 1.

---

## Phase 2: Foundation Sprint (TDD)

### Cycle
```
1. Write failing test
2. Write minimal code to pass
3. Refactor
4. Commit
5. Repeat
```

### Backend Foundation
- [ ] Database schema + migrations
- [ ] Core models with tests (Part, Price, Retailer, Build)
- [ ] Basic API endpoints with tests
- [ ] One working scraper (proof of concept)

### Frontend Foundation
- [ ] Project scaffold with test setup
- [ ] Component library (Button, Card, Input, etc.)
- [ ] Basic routing
- [ ] API client with mocks

### Exit Criteria
- All tests pass
- Can fetch one real price from one retailer
- Can display it in the UI

---

## Phase 3: MVP Build (Iterative)

### Sprint Cycle (1-2 days each)
```
Plan → Test → Build → Review → Ship → Learn → Repeat
```

### MVP Features (ordered)
1. **Search** — Find a part by name
2. **Price comparison** — Show prices from multiple retailers
3. **Build list** — Add parts, see total
4. **Compatibility check** — Basic warnings (socket mismatch, etc.)
5. **Price history** — Graph of price over time

### Definition of Done (per feature)
- [ ] Tests written and passing
- [ ] Code reviewed
- [ ] Works in production
- [ ] Documented

---

## Phase 4: Learn & Iterate

### After Each Sprint
1. **What worked?** — Keep doing it
2. **What didn't?** — Fix the process
3. **What did we learn?** — Update docs
4. **What's next?** — Prioritize backlog

### Metrics to Track
- Test coverage %
- Build time
- Scraper success rate
- User feedback (when we have users)

---

## TDD Practices

### Test Pyramid
```
         /\
        /  \  E2E (few)
       /----\
      /      \ Integration (some)
     /--------\
    /          \ Unit (many)
   --------------
```

### Naming Convention
```
test_<unit>_<scenario>_<expected_result>

Example:
test_price_scraper_newegg_returns_valid_price
test_compatibility_checker_mismatched_socket_returns_warning
test_build_calculator_sums_prices_correctly
```

### Coverage Target
- **Unit tests**: 80%+
- **Integration**: Key paths covered
- **E2E**: Critical user flows

---

## Git Workflow

```
main (protected)
  └── develop
        ├── feature/search-api
        ├── feature/price-scraper
        └── fix/socket-compatibility
```

### Commit Messages
```
feat(scraper): add newegg price fetcher
test(api): add search endpoint tests
fix(compat): handle DDR4/DDR5 mismatch
docs(arch): update system diagram
```

---

## Current Status

**Phase 1: Design & Architecture** — IN PROGRESS

Agents working on:
- PM: PRD
- Data: Source research
- Backend: Architecture
- Frontend: UI design

Next: Review all deliverables → Approve → Begin Phase 2

---

*Last updated: 2026-01-31*
