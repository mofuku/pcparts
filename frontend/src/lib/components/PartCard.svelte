<script lang="ts">
  interface Props {
    id: string;
    name: string;
    specs: string;
    priceMin: number;
    priceMax: number;
    retailers: number;
    perfScore: number;
    image?: string;
  }
  
  let { id, name, specs, priceMin, priceMax, retailers, perfScore, image = '📦' }: Props = $props();
</script>

<a 
  href="/part/{id}"
  class="group flex gap-4 rounded-xl border border-white/10 bg-bg-secondary p-4 hover:border-accent-green/30 hover:bg-bg-tertiary transition-all"
>
  <!-- Image -->
  <div class="flex h-24 w-24 shrink-0 items-center justify-center rounded-lg bg-bg-tertiary text-4xl">
    {image}
  </div>
  
  <!-- Info -->
  <div class="flex-1 min-w-0">
    <h2 class="font-medium text-text-primary group-hover:text-accent-green transition-colors truncate">
      {name}
    </h2>
    <p class="mt-1 text-sm text-text-secondary">
      {specs}
    </p>
    
    <div class="mt-3 flex flex-wrap items-center gap-4">
      <div class="price text-lg font-semibold">
        <span class="text-accent-green">${priceMin}</span>
        <span class="text-text-tertiary"> - </span>
        <span class="text-text-secondary">${priceMax}</span>
      </div>
      <span class="text-sm text-text-tertiary">
        across {retailers} retailers
      </span>
    </div>
    
    <!-- Performance Bar -->
    <div class="mt-2 flex items-center gap-2">
      <div class="h-2 w-24 overflow-hidden rounded-full bg-bg-tertiary">
        <div 
          class="h-full bg-accent-green transition-all"
          style="width: {perfScore}%"
        ></div>
      </div>
      <span class="text-sm text-text-secondary">{perfScore}/100 perf/$</span>
    </div>
  </div>
</a>
