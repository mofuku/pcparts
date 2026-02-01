<script lang="ts">
  import { page } from '$app/stores';
  
  let partId = $derived($page.params.id);
  
  // Mock data - will come from API
  const part = {
    name: 'NVIDIA GeForce RTX 4070 Founders Edition',
    category: 'Graphics Card',
    rating: 4.8,
    reviews: 2341,
    specs: {
      'Memory': '12GB GDDR6X',
      'TDP': '200W',
      'Length': '242mm',
      'CUDA Cores': '5888',
      'Boost Clock': '2.48 GHz',
      'Memory Bus': '192-bit'
    },
    prices: [
      { retailer: 'Amazon', price: 549, stock: 'In Stock', best: true },
      { retailer: 'Best Buy', price: 569, stock: 'In Stock', best: false },
      { retailer: 'Newegg', price: 579, stock: 'Low Stock', best: false },
      { retailer: 'Micro Center', price: 629, stock: 'In Stock', best: false },
    ],
    priceHistory: {
      allTimeLow: 499,
      allTimeLowDate: 'Black Friday 2024',
      average: 572
    }
  };
</script>

<svelte:head>
  <title>{part.name} — PCParts</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
  <!-- Breadcrumb -->
  <div class="flex items-center justify-between">
    <a href="/search" class="text-text-tertiary hover:text-text-primary transition-colors">
      ← Back to results
    </a>
    <button class="flex items-center gap-2 rounded-lg bg-accent-green px-4 py-2 text-sm font-medium text-black hover:bg-accent-green/90 transition-colors">
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
      </svg>
      Add to Build
    </button>
  </div>
  
  <!-- Header -->
  <div class="mt-8 flex flex-col gap-8 lg:flex-row">
    <!-- Image -->
    <div class="flex h-64 w-full shrink-0 items-center justify-center rounded-2xl bg-bg-secondary text-8xl lg:h-80 lg:w-80">
      🎮
    </div>
    
    <!-- Info -->
    <div class="flex-1">
      <p class="text-sm text-text-secondary">{part.category}</p>
      <h1 class="mt-1 text-2xl font-bold sm:text-3xl">{part.name}</h1>
      
      <div class="mt-3 flex items-center gap-2">
        <div class="flex text-accent-amber">
          {'★'.repeat(Math.floor(part.rating))}
          {part.rating % 1 >= 0.5 ? '½' : ''}
        </div>
        <span class="text-sm text-text-secondary">{part.rating} ({part.reviews.toLocaleString()} reviews)</span>
      </div>
      
      <!-- Specs Grid -->
      <div class="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
        {#each Object.entries(part.specs) as [key, value]}
          <div class="rounded-lg bg-bg-secondary p-3">
            <p class="text-xs text-text-tertiary">{key}</p>
            <p class="mt-1 font-medium">{value}</p>
          </div>
        {/each}
      </div>
    </div>
  </div>
  
  <!-- Prices Section -->
  <section class="mt-12">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold">💰 Prices</h2>
      <button class="flex items-center gap-2 rounded-lg border border-accent-blue px-4 py-2 text-sm text-accent-blue hover:bg-accent-blue/10 transition-colors">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
        </svg>
        Set Price Alert
      </button>
    </div>
    
    <div class="mt-4 overflow-hidden rounded-xl border border-white/10">
      {#each part.prices as price, i}
        <div 
          class="flex items-center justify-between border-b border-white/5 p-4 last:border-0 {price.best ? 'bg-accent-green/5' : 'bg-bg-secondary'}"
        >
          <div class="flex items-center gap-4">
            <span class="text-lg">
              {price.best ? '🟢' : '──'}
            </span>
            <span class="font-medium">{price.retailer}</span>
          </div>
          
          <div class="flex items-center gap-4">
            <span class="price text-lg font-semibold {price.best ? 'text-accent-green' : ''}">${price.price}</span>
            <span class="rounded-full px-3 py-1 text-xs {
              price.stock === 'In Stock' ? 'bg-accent-green/10 text-accent-green' : 
              price.stock === 'Low Stock' ? 'bg-accent-amber/10 text-accent-amber' : 
              'bg-accent-red/10 text-accent-red'
            }">
              {price.stock}
            </span>
            <a 
              href="#" 
              target="_blank"
              class="flex items-center gap-1 rounded-lg bg-accent-green px-4 py-2 text-sm font-medium text-black hover:bg-accent-green/90 transition-colors"
            >
              Buy
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
            </a>
          </div>
        </div>
      {/each}
    </div>
  </section>
  
  <!-- Price History -->
  <section class="mt-12">
    <h2 class="text-xl font-semibold">📈 Price History (90 days)</h2>
    
    <div class="mt-4 rounded-xl border border-white/10 bg-bg-secondary p-6">
      <!-- Chart Placeholder -->
      <div class="flex h-48 items-center justify-center text-text-tertiary">
        <div class="text-center">
          <p class="text-4xl">📊</p>
          <p class="mt-2">Chart component (use Chart.js or uPlot)</p>
        </div>
      </div>
      
      <!-- Stats -->
      <div class="mt-6 flex flex-wrap gap-8 border-t border-white/10 pt-6">
        <div>
          <p class="text-sm text-text-tertiary">All-time Low</p>
          <p class="price mt-1 text-lg font-semibold text-accent-green">
            ${part.priceHistory.allTimeLow}
          </p>
          <p class="text-xs text-text-tertiary">{part.priceHistory.allTimeLowDate}</p>
        </div>
        <div>
          <p class="text-sm text-text-tertiary">Average Price</p>
          <p class="price mt-1 text-lg font-semibold">${part.priceHistory.average}</p>
        </div>
        <div>
          <p class="text-sm text-text-tertiary">Current Best</p>
          <p class="price mt-1 text-lg font-semibold text-accent-green">
            ${part.prices[0].price}
          </p>
          <p class="text-xs text-accent-green">
            ${part.priceHistory.average - part.prices[0].price} below average
          </p>
        </div>
      </div>
    </div>
  </section>
</div>
