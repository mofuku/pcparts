# PCParts — Product Requirements Document (MVP)

**Version:** 1.0  
**Date:** 2025-01-19  
**Author:** PM Agent  
**Status:** Draft

---

## Executive Summary

PCParts is a PC component price aggregator that helps users build PCs with confidence. We aggregate prices from regional retailers, automatically check compatibility, and help users get the best value for their budget.

**Why now?** PCPartPicker dominates but has become bloated, US-centric, and affiliate-driven. There's room for a fast, clean, regionally-focused alternative that prioritizes user experience over ad revenue.

**MVP Goal:** A functional build tool where users can select parts, see aggregated prices from 5+ retailers, and get basic compatibility warnings. Ship in 4-6 weeks.

---

## User Personas

### 1. 🎮 First-Time Builder "Alex" (Primary)
- **Who:** 18-25, wants to build their first gaming PC
- **Budget:** $800-1200
- **Pain points:**
  - Terrified of buying incompatible parts
  - Overwhelmed by options (what's a chipset?)
  - Doesn't know which retailers to trust
- **Needs:** Hand-holding, clear compatibility indicators, "safe" recommendations
- **Quote:** *"I just want to know this will all work together"*

### 2. 💰 Budget Hunter "Jordan" (Primary)
- **Who:** 20-35, knows what they want, hunting the best deal
- **Budget:** Flexible, but wants maximum value
- **Pain points:**
  - Opens 15 tabs comparing prices
  - Misses flash sales
  - PCPartPicker prices often outdated
- **Needs:** Real-time prices, price history, deal alerts
- **Quote:** *"I know what I want, just tell me where it's cheapest"*

### 3. 🔧 Upgrader "Sam" (Secondary)
- **Who:** Has existing PC, wants to upgrade GPU/RAM/storage
- **Budget:** $200-500 for specific parts
- **Pain points:**
  - Will this fit in my case? Will my PSU handle it?
  - Diminishing returns confusion (is 32GB RAM worth it?)
- **Needs:** Single-part search, compatibility with existing builds
- **Quote:** *"Can I just upgrade my GPU without replacing everything?"*

### 4. 🏗️ Enthusiast "Morgan" (Secondary)
- **Who:** 25-40, builds PCs for fun, follows hardware news
- **Budget:** $2000+ for high-end builds
- **Pain points:**
  - PCPartPicker UI is cluttered
  - Wants raw data, not hand-holding
  - Cares about thermals, overclocking headroom
- **Needs:** Advanced filters, detailed specs, no BS
- **Quote:** *"Just give me the data, I'll decide"*

---

## User Stories (MVP)

### P0 — Must Have for Launch

| ID | As a... | I want to... | So that... |
|----|---------|--------------|------------|
| US-01 | First-time builder | Select parts from each category (CPU, GPU, etc.) | I can assemble a complete build |
| US-02 | Budget hunter | See prices from multiple retailers for each part | I can find the cheapest option |
| US-03 | First-time builder | Get warned when parts are incompatible | I don't waste money on parts that won't work |
| US-04 | Any user | See the total price of my build | I know if I'm within budget |
| US-05 | Any user | Share my build via URL | I can get feedback from friends/Reddit |
| US-06 | Budget hunter | See price history for a part | I know if current price is good or inflated |

### P1 — Important for Traction

| ID | As a... | I want to... | So that... |
|----|---------|--------------|------------|
| US-07 | First-time builder | Start from a preset build template | I don't have to start from scratch |
| US-08 | Budget hunter | Set a price alert on a part | I get notified when it drops |
| US-09 | Any user | Filter parts by price, brand, specs | I can narrow down options quickly |
| US-10 | Budget hunter | See "value score" (performance/$) | I can identify the sweet spot |
| US-11 | Upgrader | Input my existing parts | I can see what upgrades are compatible |

### P2 — Nice to Have

| ID | As a... | I want to... | So that... |
|----|---------|--------------|------------|
| US-12 | First-time builder | Get AI recommendations for my budget | I don't have to research every part |
| US-13 | Enthusiast | Compare two builds side-by-side | I can evaluate tradeoffs |
| US-14 | Any user | See estimated gaming performance | I know what FPS to expect |
| US-15 | Any user | Export my build to spreadsheet | I can track purchases offline |

---

## MVP Feature List

### P0 — Launch Blockers (Week 1-3)

#### Part Catalog
- [ ] **CPU:** List all current-gen CPUs (Intel 12th-14th gen, AMD 5000/7000 series)
- [ ] **GPU:** All current-gen GPUs (RTX 30/40 series, RX 6000/7000 series)
- [ ] **Motherboard:** Matching boards for supported CPUs
- [ ] **RAM:** DDR4 and DDR5 kits (16GB, 32GB, 64GB)
- [ ] **Storage:** NVMe SSDs, SATA SSDs, HDDs
- [ ] **PSU:** 500W-1000W units from major brands
- [ ] **Case:** Popular ATX/mATX/ITX cases
- [ ] **Cooler:** Air and AIO coolers

#### Price Aggregation
- [ ] Scrape prices from 5+ retailers (region-specific)
- [ ] Update prices at least every 6 hours
- [ ] Show "in stock" vs "out of stock" status
- [ ] Display shipping cost where available

#### Compatibility Engine
- [ ] CPU ↔ Motherboard socket matching
- [ ] RAM type matching (DDR4 vs DDR5)
- [ ] PSU wattage estimation
- [ ] Basic warnings displayed in UI

#### Build Interface
- [ ] Part picker with category tabs
- [ ] Current build sidebar with running total
- [ ] Compatibility status indicator (✅/⚠️/❌)
- [ ] Shareable build URL

### P1 — Growth Features (Week 4-6)

- [ ] Price history chart (30/90 days)
- [ ] Part filters (price range, brand, socket)
- [ ] 3-5 preset build templates ("$800 Gaming", "$1500 Workstation")
- [ ] Basic search functionality
- [ ] Email price alerts (requires auth)

### P2 — Future Scope

- [ ] AI build assistant ("Build me a $1000 gaming PC")
- [ ] User accounts and saved builds
- [ ] Community build sharing/voting
- [ ] Performance benchmarks integration
- [ ] Multi-region support

---

## Compatibility Rules (Priority Order)

### Phase 1 — Hard Blocks (MVP)

These prevent the build from functioning at all:

| Rule | Check | Severity |
|------|-------|----------|
| **CPU-Motherboard Socket** | CPU socket must match motherboard socket (e.g., LGA1700 = LGA1700) | 🔴 Error |
| **CPU-Motherboard Chipset** | Chipset must support CPU generation (e.g., B660 supports 12th/13th gen, not 14th refresh) | 🔴 Error |
| **RAM-Motherboard Type** | DDR4 motherboard can't use DDR5 RAM | 🔴 Error |
| **RAM Speed Support** | RAM speed must be within motherboard's supported range | 🟡 Warning |

### Phase 2 — Functional Warnings (MVP)

| Rule | Check | Severity |
|------|-------|----------|
| **PSU Wattage** | Total TDP + 20% headroom ≤ PSU wattage | 🟡 Warning |
| **PSU Connectors** | GPU power connectors available (8-pin, 12VHPWR) | 🟡 Warning |
| **RAM Slots** | Number of RAM sticks ≤ motherboard slots | 🔴 Error |
| **M.2 Slots** | Number of NVMe drives ≤ M.2 slots | 🔴 Error |

### Phase 3 — Physical Fit (Post-MVP)

| Rule | Check | Severity |
|------|-------|----------|
| **GPU Length** | GPU length ≤ case max GPU clearance | 🟡 Warning |
| **Cooler Height** | Cooler height ≤ case max cooler clearance | 🟡 Warning |
| **Radiator Support** | AIO radiator size supported by case | 🟡 Warning |
| **PSU Length** | PSU length ≤ case PSU clearance | 🟡 Warning |

### Compatibility Data Sources
- Manufacturer spec sheets (primary)
- PCPartPicker (reference/validation)
- Community wikis (r/buildapc, LTT forums)

---

## Success Metrics

### Launch Goals (Week 6)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Parts in catalog** | 500+ SKUs | Database count |
| **Retailers scraped** | 5+ | Active scraper count |
| **Price freshness** | <6 hours old | Scrape timestamp delta |
| **Page load time** | <2 seconds | Lighthouse/RUM |
| **Compatibility accuracy** | >95% | Manual audit of 50 builds |

### Growth Goals (Month 2-3)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Weekly active users** | 1,000 | Analytics |
| **Builds created** | 500/week | Database count |
| **Builds shared** | 100/week | Share link clicks |
| **Return visitors** | 30% | Analytics |
| **Price alert signups** | 200 | Database count |

### North Star Metric
**Builds completed with purchase intent** — Users who click through to a retailer to buy. This indicates we've delivered real value.

---

## Out of Scope (MVP)

Explicitly NOT building these for MVP:

| Feature | Why Not |
|---------|---------|
| **User accounts** | Adds auth complexity; shareable URLs sufficient for MVP |
| **Multiple regions** | Do one region exceptionally well first |
| **Peripherals** (monitors, keyboards) | Focus on core PC parts; expand later |
| **Pre-built PC comparisons** | Different product category |
| **Forums/community features** | Reddit exists; focus on tool utility |
| **Affiliate revenue** | Get users first, monetize later |
| **Mobile app** | Responsive web is sufficient |
| **Performance benchmarks** | Requires licensed data or complex scraping |
| **Custom water cooling** | Niche; complex compatibility |
| **Used/refurbished parts** | Pricing unreliable; trust issues |

---

## Competitive Positioning

### PCPartPicker Weaknesses (Our Opportunities)

| Their Problem | Our Solution |
|---------------|--------------|
| **Slow, cluttered UI** | Fast, minimal interface |
| **US-centric** | Regional focus from day one |
| **Stale prices** | Aggressive scraping, fresher data |
| **Affiliate-driven recommendations** | Neutral; best value wins |
| **No AI assistance** | AI build recommendations (P2) |
| **Overwhelming for beginners** | Guided templates, clear warnings |

### Our Wedge
Start with **one region** (e.g., Australia, UK, or specific EU country) where PCPartPicker coverage is weak. Dominate that market before expanding.

---

## Open Questions

1. **Which region to launch?** Needs market research on retailer API availability
2. **Scraping legality?** Need to review retailer ToS; may need partnerships
3. **Data storage costs?** Price history could grow large; need retention policy
4. **Performance data source?** Benchmarks are valuable but complex to source

---

## Appendix: Part Category Specs

### Minimum Data Per Part

**All Parts:**
- Name, brand, model
- Image URL
- Current price (per retailer)
- In-stock status
- Product page URL

**CPUs:** Socket, cores, threads, base/boost clock, TDP, integrated graphics (yes/no)

**GPUs:** VRAM, TDP, length (mm), power connectors, slot width

**Motherboards:** Socket, chipset, form factor, RAM type, RAM slots, M.2 slots, max RAM speed

**RAM:** Type (DDR4/5), speed, capacity, sticks count, CAS latency

**Storage:** Type (NVMe/SATA/HDD), capacity, interface, form factor

**PSUs:** Wattage, efficiency rating, modular (yes/no), connectors list

**Cases:** Form factor support, max GPU length, max cooler height, radiator support

**Coolers:** Type (air/AIO), height (air) or radiator size (AIO), TDP rating, socket compatibility

---

*This document is the source of truth for MVP scope. Feature requests outside this scope should be logged but deferred to post-MVP.*
