<script lang="ts">
  interface Price {
    retailer: string;
    price: number;
    stock: 'In Stock' | 'Low Stock' | 'Out of Stock';
    url: string;
    best?: boolean;
  }
  
  interface Props {
    prices: Price[];
  }
  
  let { prices }: Props = $props();
</script>

<div class="overflow-hidden rounded-xl border border-white/10">
  {#each prices as price}
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
        <span class="price text-lg font-semibold {price.best ? 'text-accent-green' : ''}">
          ${price.price}
        </span>
        <span class="rounded-full px-3 py-1 text-xs {
          price.stock === 'In Stock' ? 'bg-accent-green/10 text-accent-green' : 
          price.stock === 'Low Stock' ? 'bg-accent-amber/10 text-accent-amber' : 
          'bg-accent-red/10 text-accent-red'
        }">
          {price.stock}
        </span>
        <a 
          href={price.url}
          target="_blank"
          rel="noopener noreferrer"
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
