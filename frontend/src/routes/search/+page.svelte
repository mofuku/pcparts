<script lang="ts">
  import { page } from '$app/stores';
  
  let query = $derived($page.url.searchParams.get('q') || '');
  let category = $derived($page.url.searchParams.get('category') || '');
  let filtersOpen = $state(false);
  
  // Mock data - will be replaced with API calls
  const results = [
    {
      id: 'rtx-4070-fe',
      name: 'NVIDIA GeForce RTX 4070 Founders Edition',
      specs: '12GB GDDR6X • 200W TDP',
      priceRange: { min: 549, max: 629 },
      retailers: 6,
      perfScore: 87,
      image: '🎮'
    },
    {
      id: 'rtx-4070-tuf',
      name: 'ASUS TUF Gaming RTX 4070 OC',
      specs: '12GB GDDR6X • 215W TDP',
      priceRange: { min: 569, max: 649 },
      retailers: 5,
      perfScore: 84,
      image: '🎮'
    },
    {
      id: 'rtx-4070-gaming-x',
      name: 'MSI Gaming X Trio RTX 4070',
      specs: '12GB GDDR6X • 220W TDP',
      priceRange: { min: 579, max: 659 },
      retailers: 4,
      perfScore: 82,
      image: '🎮'
    },
  ];
</script>

<svelte:head>
  <title>{query || category || 'Search'} — PCParts</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
  <!-- Header -->
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-4">
      <a href="/" class="text-text-tertiary hover:text-text-primary transition-colors">
        ← Back
      </a>
      <h1 class="text-xl font-semibold">
        {#if query}
          "{query}"
        {:else if category}
          {category.charAt(0).toUpperCase() + category.slice(1)}
        {:else}
          All Parts
        {/if}
      </h1>
    </div>
    
    <div class="flex items-center gap-3">
      <button 
        onclick={() => filtersOpen = !filtersOpen}
        class="flex items-center gap-2 rounded-lg border border-white/10 px-4 py-2 text-sm hover:border-white/20 transition-colors lg:hidden"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
        </svg>
        Filters
      </button>
      
      <select class="rounded-lg border border-white/10 bg-bg-secondary px-4 py-2 text-sm focus:border-accent-green focus:outline-none">
        <option>Price: Low to High</option>
        <option>Price: High to Low</option>
        <option>Best Value (Perf/$)</option>
        <option>Newest</option>
      </select>
    </div>
  </div>
  
  <div class="mt-6 flex gap-8">
    <!-- Filters Sidebar -->
    <aside class="hidden w-64 shrink-0 lg:block">
      <div class="sticky top-24 space-y-6">
        <div>
          <h3 class="text-sm font-medium text-text-primary">Price Range</h3>
          <div class="mt-3 flex items-center gap-3">
            <input 
              type="number" 
              placeholder="Min"
              class="w-full rounded-lg border border-white/10 bg-bg-secondary px-3 py-2 text-sm placeholder-text-tertiary focus:border-accent-green focus:outline-none"
            />
            <span class="text-text-tertiary">—</span>
            <input 
              type="number" 
              placeholder="Max"
              class="w-full rounded-lg border border-white/10 bg-bg-secondary px-3 py-2 text-sm placeholder-text-tertiary focus:border-accent-green focus:outline-none"
            />
          </div>
        </div>
        
        <div>
          <h3 class="text-sm font-medium text-text-primary">Brand</h3>
          <div class="mt-3 space-y-2">
            {#each ['NVIDIA', 'ASUS', 'MSI', 'Gigabyte', 'EVGA'] as brand}
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" class="rounded border-white/20 bg-bg-secondary text-accent-green focus:ring-accent-green/50" />
                <span class="text-sm text-text-secondary">{brand}</span>
              </label>
            {/each}
          </div>
        </div>
        
        <div>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" class="rounded border-white/20 bg-bg-secondary text-accent-green focus:ring-accent-green/50" />
            <span class="text-sm text-text-primary">In Stock Only</span>
          </label>
        </div>
        
        <div>
          <h3 class="text-sm font-medium text-text-primary">Min Performance/$</h3>
          <input 
            type="range" 
            min="0" 
            max="100" 
            value="0"
            class="mt-3 w-full accent-accent-green"
          />
          <div class="flex justify-between text-xs text-text-tertiary">
            <span>Any</span>
            <span>100</span>
          </div>
        </div>
      </div>
    </aside>
    
    <!-- Results -->
    <div class="flex-1">
      <p class="text-sm text-text-secondary">
        Showing {results.length} results
      </p>
      
      <div class="mt-4 space-y-4">
        {#each results as result}
          <a 
            href="/part/{result.id}"
            class="group flex gap-4 rounded-xl border border-white/10 bg-bg-secondary p-4 hover:border-accent-green/30 hover:bg-bg-tertiary transition-all"
          >
            <!-- Image -->
            <div class="flex h-24 w-24 shrink-0 items-center justify-center rounded-lg bg-bg-tertiary text-4xl">
              {result.image}
            </div>
            
            <!-- Info -->
            <div class="flex-1 min-w-0">
              <h2 class="font-medium text-text-primary group-hover:text-accent-green transition-colors truncate">
                {result.name}
              </h2>
              <p class="mt-1 text-sm text-text-secondary">
                {result.specs}
              </p>
              
              <div class="mt-3 flex flex-wrap items-center gap-4">
                <div class="price text-lg font-semibold">
                  <span class="text-accent-green">${result.priceRange.min}</span>
                  <span class="text-text-tertiary"> - </span>
                  <span class="text-text-secondary">${result.priceRange.max}</span>
                </div>
                <span class="text-sm text-text-tertiary">
                  across {result.retailers} retailers
                </span>
              </div>
              
              <!-- Performance Bar -->
              <div class="mt-2 flex items-center gap-2">
                <div class="h-2 w-24 overflow-hidden rounded-full bg-bg-tertiary">
                  <div 
                    class="h-full bg-accent-green"
                    style="width: {result.perfScore}%"
                  ></div>
                </div>
                <span class="text-sm text-text-secondary">{result.perfScore}/100 perf/$</span>
              </div>
            </div>
            
            <!-- Action -->
            <div class="hidden sm:flex items-center">
              <button class="rounded-lg border border-white/10 px-4 py-2 text-sm text-text-secondary hover:border-accent-green hover:text-accent-green transition-colors">
                Compare
              </button>
            </div>
          </a>
        {/each}
      </div>
    </div>
  </div>
</div>
