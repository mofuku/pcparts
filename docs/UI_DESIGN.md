# PCParts UI Design System

## Design Philosophy

**Anti-PCPartPicker**: They're cluttered with ads, affiliate badges, and feature creep. We're the opposite.

- **Fast** — Sub-100ms interactions, lazy load everything
- **Clean** — White space is not wasted space
- **Focused** — One task per screen, minimal navigation
- **Dark-first** — Gamers live in dark mode
- **Mobile-native** — Touch targets, responsive by default

---

## Color Palette

```css
/* Dark Theme (Default) */
--bg-primary: #0a0a0b;      /* Near-black */
--bg-secondary: #141416;    /* Cards, elevated surfaces */
--bg-tertiary: #1c1c1f;     /* Input fields, hover states */

--text-primary: #f4f4f5;    /* Main text */
--text-secondary: #a1a1aa;  /* Muted text */
--text-tertiary: #52525b;   /* Disabled/hints */

--accent-primary: #22c55e;  /* Green — deals, savings, CTAs */
--accent-warning: #f59e0b;  /* Amber — compatibility warnings */
--accent-danger: #ef4444;   /* Red — errors, incompatible */
--accent-info: #3b82f6;     /* Blue — links, info */

/* Price indicators */
--price-low: #22c55e;       /* Best price */
--price-mid: #f59e0b;       /* Average */
--price-high: #ef4444;      /* Overpriced */
```

## Typography

```css
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;  /* Prices, specs */

--text-xs: 0.75rem;    /* 12px — Fine print */
--text-sm: 0.875rem;   /* 14px — Secondary info */
--text-base: 1rem;     /* 16px — Body */
--text-lg: 1.125rem;   /* 18px — Emphasis */
--text-xl: 1.25rem;    /* 20px — Card titles */
--text-2xl: 1.5rem;    /* 24px — Page titles */
--text-3xl: 1.875rem;  /* 30px — Hero */
```

---

## Page Designs

### 1. Home / Search

**Purpose**: Get users to their part FAST

```
┌─────────────────────────────────────────────────────────┐
│  PCParts                              [Build] [Sign In] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              Find PC parts at the best price            │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │ 🔍 Search parts... (RTX 4070, Ryzen 7, 32GB)   │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
│   [CPU] [GPU] [RAM] [Storage] [Mobo] [PSU] [Case]      │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  🔥 Hot Deals                            [View all →]   │
│                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ RTX 4070 │ │ i5-14600K│ │ 32GB DDR5│ │ 1TB NVMe │   │
│  │ $549→$499│ │ $319→$289│ │ $89→$79  │ │ $79→$69  │   │
│  │ ↓9% 🔥   │ │ ↓9%      │ │ ↓11%     │ │ ↓13%     │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│                                                         │
│  📈 Trending Searches                                   │
│  RTX 5080 • DDR5 • AM5 motherboard • 4TB NVMe          │
└─────────────────────────────────────────────────────────┘
```

**Key interactions**:
- Search is autofocus on load
- Instant search results as you type (debounced 200ms)
- Category chips filter search
- Deal cards link to part detail

---

### 2. Search Results

**Purpose**: Compare options quickly

```
┌─────────────────────────────────────────────────────────┐
│  ← "RTX 4070"                        [Filters ▾] [Sort]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Showing 24 results                                     │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ [img] NVIDIA GeForce RTX 4070 Founders Edition   │  │
│  │       12GB GDDR6X • 200W TDP                      │  │
│  │                                                   │  │
│  │       $549 - $629 across 6 retailers              │  │
│  │       ████████░░ 87/100 perf/$                    │  │
│  │                                        [Compare]  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ [img] ASUS TUF Gaming RTX 4070 OC                │  │
│  │       12GB GDDR6X • 215W TDP                      │  │
│  │                                                   │  │
│  │       $569 - $649 across 5 retailers              │  │
│  │       ████████░░ 84/100 perf/$                    │  │
│  │                                        [Compare]  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Filters sidebar** (collapsed on mobile):
- Price range slider
- Brand checkboxes
- In-stock only toggle
- Performance/$ threshold

---

### 3. Part Detail

**Purpose**: Show all prices + history, one click to buy

```
┌─────────────────────────────────────────────────────────┐
│  ← Back                                    [+ Add to Build] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────┐  NVIDIA GeForce RTX 4070 FE               │
│  │        │  Graphics Card                              │
│  │  [img] │                                             │
│  │        │  ⭐ 4.8 (2,341 reviews)                     │
│  └────────┘                                             │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│  SPECS                                                  │
│  Memory: 12GB GDDR6X  │  TDP: 200W  │  Length: 242mm   │
│  CUDA: 5888           │  Boost: 2.48GHz               │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  💰 PRICES                              [🔔 Set Alert]  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🟢 Amazon           $549    [In Stock]  [Buy →] │   │
│  │ ── Best Buy         $569    [In Stock]  [Buy →] │   │
│  │ ── Newegg           $579    [Low Stock] [Buy →] │   │
│  │ 🔴 Micro Center     $629    [In Stock]  [Buy →] │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  📈 PRICE HISTORY (90 days)                            │
│                                                         │
│  $650 ┤                                                 │
│  $600 ┤    ╭──╮                                        │
│  $550 ┤───╯    ╰───────────────────╮                   │
│  $500 ┤                            ╰───● $549 (now)    │
│       └─────────────────────────────────────────────   │
│         Jan        Feb        Mar        Apr           │
│                                                         │
│  All-time low: $499 (Black Friday 2024)                │
│  Avg price: $572                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Key features**:
- Best price highlighted in green
- Price history chart (interactive, hover for values)
- One-click external buy links
- Price alert button
- Quick add to current build

---

### 4. Build Configurator

**Purpose**: Assemble a build, track total, check compatibility

```
┌─────────────────────────────────────────────────────────┐
│  My Build: "Gaming Rig 2025"         [Save] [Share] [Clear] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─ COMPATIBILITY ──────────────────────────────────┐  │
│  │ ✅ All parts compatible                          │  │
│  │ ⚡ Estimated wattage: 450W (PSU: 750W) ✓         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  COMPONENT          SELECTION                   PRICE  │
│  ───────────────────────────────────────────────────── │
│  CPU         │ AMD Ryzen 7 7800X3D           │  $359  │
│              │ [Change]                       │        │
│  ────────────┼───────────────────────────────┼─────── │
│  CPU Cooler  │ Noctua NH-D15S               │   $99  │
│              │ [Change]                       │        │
│  ────────────┼───────────────────────────────┼─────── │
│  GPU         │ RTX 4070 FE                   │  $549  │
│              │ [Change]                       │        │
│  ────────────┼───────────────────────────────┼─────── │
│  Motherboard │ + Select motherboard          │    —   │
│              │ (Showing AM5 boards only)     │        │
│  ────────────┼───────────────────────────────┼─────── │
│  RAM         │ + Select RAM                  │    —   │
│              │ (Showing DDR5 only)           │        │
│  ────────────┼───────────────────────────────┼─────── │
│  Storage     │ + Add storage                 │    —   │
│  ────────────┼───────────────────────────────┼─────── │
│  PSU         │ + Select PSU                  │    —   │
│  ────────────┼───────────────────────────────┼─────── │
│  Case        │ + Select case                 │    —   │
│  ═══════════════════════════════════════════════════  │
│                                                         │
│               TOTAL: $1,007    [Buy All at Amazon →]   │
│               Cheapest combo: $987 (mixed retailers)    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Smart features**:
- Auto-filters compatible parts when selecting
- Wattage calculator updates live
- Compatibility warnings (yellow) and errors (red)
- "Buy all" finds cheapest retailer combo
- Shareable build links

---

## Components Library

### Buttons

```
Primary:   [████ Add to Build ████]  — Green bg, white text
Secondary: [──── Compare ────]       — Border only, gray
Ghost:     [ Change ]                — No border, subtle hover
Danger:    [████ Remove ████]        — Red bg
```

### Cards

```
┌────────────────────────────┐
│ [image]                    │  ← Aspect ratio 4:3
│                            │
│ Product Name               │  ← text-lg, font-medium
│ Brief specs                │  ← text-sm, text-secondary
│                            │
│ $XXX - $XXX                │  ← text-lg, font-mono
│ ██████░░ 85 perf/$         │  ← Progress bar + score
└────────────────────────────┘
```

### Price Badge

```
Best:    🟢 $549  (green)
Average: ── $569  (gray)
High:    🔴 $629  (red)
```

### Compatibility Indicator

```
✅ Compatible
⚠️ Check clearance (warning)
❌ Incompatible: Wrong socket (error)
```

---

## User Flows

### Flow 1: Quick Search → Buy

```
Home → Type search → Click result → See prices → Click "Buy" → External site
```
**Target time: <10 seconds**

### Flow 2: Build a PC

```
Home → Click "Build" → Add CPU → Add GPU (auto-filtered) → Add RAM →
→ See compatibility ✅ → See total → Share link or Buy
```

### Flow 3: Track a Deal

```
Search → Part detail → Click "Set Alert" → Enter target price → 
→ Get email when price drops
```

### Flow 4: Compare Parts

```
Search → Check "Compare" on 2-3 items → Click "Compare X items" →
→ Side-by-side specs + prices
```

---

## Responsive Breakpoints

```css
--mobile:  < 640px   /* Single column, bottom nav */
--tablet:  640-1024px /* 2 columns, sidebar collapses */
--desktop: > 1024px   /* Full layout, persistent sidebar */
```

### Mobile Adaptations

- Search bar sticks to top
- Filters become bottom sheet
- Build configurator becomes accordion
- Price table scrolls horizontally
- Touch targets minimum 44x44px

---

## Animations

Keep them subtle and fast:

```css
--transition-fast: 150ms ease-out;  /* Hovers, toggles */
--transition-base: 200ms ease-out;  /* Modals, dropdowns */
--transition-slow: 300ms ease-out;  /* Page transitions */
```

- No animation on first paint (reduce LCP)
- Prefer opacity/transform (GPU accelerated)
- `prefers-reduced-motion` respected

---

## Accessibility

- WCAG 2.1 AA minimum
- Contrast ratio 4.5:1 for text
- All interactive elements keyboard accessible
- Focus rings visible (not removed!)
- Skip links for navigation
- ARIA labels on icon-only buttons
- Screen reader announcements for live updates

---

## Tech Implementation Notes

### Framework: SvelteKit
- File-based routing
- SSR for SEO (part pages need indexing)
- ISR for price data (revalidate every 5 min)

### Styling: Tailwind CSS
- Custom theme in `tailwind.config.js`
- Component classes via `@apply` sparingly
- Dark mode via `class` strategy (not media query)

### Charts: Chart.js or Lightweight alternative
- Price history: Line chart
- Keep bundle small — consider uPlot

### Icons: Lucide (tree-shakeable)

### State: Svelte stores
- Build state persisted to localStorage
- User prefs (dark mode, region) in cookies

---

## File Structure

```
frontend/
├── src/
│   ├── routes/
│   │   ├── +page.svelte          # Home
│   │   ├── +layout.svelte        # Shell (nav, footer)
│   │   ├── search/
│   │   │   └── +page.svelte      # Search results
│   │   ├── part/
│   │   │   └── [id]/+page.svelte # Part detail
│   │   ├── build/
│   │   │   └── +page.svelte      # Build configurator
│   │   └── compare/
│   │       └── +page.svelte      # Compare view
│   ├── lib/
│   │   ├── components/
│   │   │   ├── SearchBar.svelte
│   │   │   ├── PartCard.svelte
│   │   │   ├── PriceTable.svelte
│   │   │   ├── PriceChart.svelte
│   │   │   ├── BuildList.svelte
│   │   │   └── CompatibilityBadge.svelte
│   │   ├── stores/
│   │   │   ├── build.js          # Current build state
│   │   │   └── preferences.js    # User settings
│   │   └── utils/
│   │       ├── api.js            # Backend calls
│   │       └── compatibility.js  # Client-side checks
│   └── app.css                   # Global styles + Tailwind
├── static/
│   └── favicon.svg
├── tailwind.config.js
├── svelte.config.js
└── package.json
```

---

*Designed for speed, built for builders.* 🖥️
