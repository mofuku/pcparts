<script lang="ts">
  let searchQuery = $state('');
  
  const categories = [
    { name: 'CPU', icon: '🔲', slug: 'cpu' },
    { name: 'GPU', icon: '🎮', slug: 'gpu' },
    { name: 'RAM', icon: '📊', slug: 'ram' },
    { name: 'Storage', icon: '💾', slug: 'storage' },
    { name: 'Motherboard', icon: '🔌', slug: 'motherboard' },
    { name: 'PSU', icon: '⚡', slug: 'psu' },
    { name: 'Case', icon: '🖥️', slug: 'case' },
  ];
  
  const deals = [
    { name: 'RTX 4070', oldPrice: 549, newPrice: 499, discount: 9, image: '🎮' },
    { name: 'i5-14600K', oldPrice: 319, newPrice: 289, discount: 9, image: '🔲' },
    { name: '32GB DDR5', oldPrice: 89, newPrice: 79, discount: 11, image: '📊' },
    { name: '1TB NVMe', oldPrice: 79, newPrice: 69, discount: 13, image: '💾' },
  ];
  
  function handleSearch(e: Event) {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
    }
  }
</script>

<svelte:head>
  <title>PCParts — Find the best parts at the best price</title>
  <meta name="description" content="Compare PC part prices across all major retailers. Build your PC, track deals, and never overpay." />
</svelte:head>

<div class="min-h-[calc(100vh-4rem)]">
  <!-- Hero Section -->
  <section class="relative overflow-hidden">
    <div class="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div class="text-center">
        <h1 class="text-3xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
          Find PC parts at the
          <span class="text-accent-green">best price</span>
        </h1>
        <p class="mx-auto mt-4 max-w-xl text-lg text-text-secondary">
          Compare prices across all major retailers. No ads, no clutter, just savings.
        </p>
        
        <!-- Search Bar -->
        <form onsubmit={handleSearch} class="mx-auto mt-8 max-w-2xl">
          <div class="relative">
            <input
              type="text"
              bind:value={searchQuery}
              placeholder="Search parts... (RTX 4070, Ryzen 7, 32GB DDR5)"
              class="w-full rounded-xl border border-white/10 bg-bg-secondary px-6 py-4 pl-14 text-lg placeholder-text-tertiary focus:border-accent-green focus:outline-none focus:ring-2 focus:ring-accent-green/20 transition-all"
            />
            <svg class="absolute left-5 top-1/2 h-5 w-5 -translate-y-1/2 text-text-tertiary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <button 
              type="submit"
              class="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg bg-accent-green px-4 py-2 font-medium text-black hover:bg-accent-green/90 transition-colors"
            >
              Search
            </button>
          </div>
        </form>
        
        <!-- Category Pills -->
        <div class="mx-auto mt-6 flex max-w-2xl flex-wrap justify-center gap-2">
          {#each categories as cat}
            <a 
              href="/search?category={cat.slug}"
              class="flex items-center gap-2 rounded-full border border-white/10 bg-bg-secondary px-4 py-2 text-sm text-text-secondary hover:border-accent-green/50 hover:text-text-primary transition-all"
            >
              <span>{cat.icon}</span>
              <span>{cat.name}</span>
            </a>
          {/each}
        </div>
      </div>
    </div>
  </section>
  
  <!-- Hot Deals -->
  <section class="border-t border-white/5 bg-bg-secondary/50">
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between">
        <h2 class="flex items-center gap-2 text-xl font-semibold">
          <span class="text-2xl">🔥</span>
          Hot Deals
        </h2>
        <a href="/deals" class="text-sm text-accent-green hover:underline">
          View all →
        </a>
      </div>
      
      <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {#each deals as deal}
          <a 
            href="/part/{deal.name.toLowerCase().replace(/\s+/g, '-')}"
            class="group rounded-xl border border-white/10 bg-bg-secondary p-4 hover:border-accent-green/30 hover:bg-bg-tertiary transition-all"
          >
            <div class="flex h-24 items-center justify-center text-5xl">
              {deal.image}
            </div>
            <h3 class="mt-3 font-medium text-text-primary group-hover:text-accent-green transition-colors">
              {deal.name}
            </h3>
            <div class="mt-2 flex items-baseline gap-2">
              <span class="price text-lg font-semibold text-accent-green">${deal.newPrice}</span>
              <span class="price text-sm text-text-tertiary line-through">${deal.oldPrice}</span>
            </div>
            <div class="mt-1 inline-flex items-center gap-1 rounded-full bg-accent-green/10 px-2 py-0.5 text-xs font-medium text-accent-green">
              ↓{deal.discount}%
              {#if deal.discount > 10}
                <span>🔥</span>
              {/if}
            </div>
          </a>
        {/each}
      </div>
    </div>
  </section>
  
  <!-- Trending -->
  <section class="border-t border-white/5">
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <h2 class="flex items-center gap-2 text-lg font-medium text-text-secondary">
        <span>📈</span>
        Trending Searches
      </h2>
      <div class="mt-4 flex flex-wrap gap-3">
        {#each ['RTX 5080', 'DDR5 6000MHz', 'AM5 motherboard', '4TB NVMe', 'Ryzen 9800X3D', 'RTX 4060 Ti'] as trend}
          <a 
            href="/search?q={encodeURIComponent(trend)}"
            class="rounded-lg border border-white/10 px-3 py-1.5 text-sm text-text-secondary hover:border-accent-blue/50 hover:text-accent-blue transition-colors"
          >
            {trend}
          </a>
        {/each}
      </div>
    </div>
  </section>
</div>
