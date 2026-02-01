<script lang="ts">
  const componentSlots = [
    { type: 'CPU', icon: '🔲', selection: { name: 'AMD Ryzen 7 7800X3D', price: 359 }, required: true },
    { type: 'CPU Cooler', icon: '❄️', selection: { name: 'Noctua NH-D15S', price: 99 }, required: false },
    { type: 'GPU', icon: '🎮', selection: { name: 'RTX 4070 FE', price: 549 }, required: true },
    { type: 'Motherboard', icon: '🔌', selection: null, hint: 'Showing AM5 boards only', required: true },
    { type: 'RAM', icon: '📊', selection: null, hint: 'Showing DDR5 only', required: true },
    { type: 'Storage', icon: '💾', selection: null, required: true },
    { type: 'PSU', icon: '⚡', selection: null, required: true },
    { type: 'Case', icon: '🖥️', selection: null, required: false },
  ];
  
  let buildName = $state('Gaming Rig 2025');
  let totalPrice = $derived(
    componentSlots
      .filter(c => c.selection)
      .reduce((sum, c) => sum + (c.selection?.price || 0), 0)
  );
  
  // Compatibility status
  const compatibility = {
    status: 'ok', // 'ok' | 'warning' | 'error'
    message: 'All parts compatible',
    wattage: { used: 450, available: 750 }
  };
</script>

<svelte:head>
  <title>{buildName} — PCParts Build</title>
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
  <!-- Header -->
  <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <div class="flex items-center gap-3">
      <span class="text-2xl">🛠️</span>
      <input 
        type="text"
        bind:value={buildName}
        class="bg-transparent text-xl font-bold focus:outline-none border-b border-transparent focus:border-accent-green"
      />
    </div>
    
    <div class="flex gap-2">
      <button class="rounded-lg border border-white/10 px-4 py-2 text-sm hover:border-white/20 transition-colors">
        Save
      </button>
      <button class="rounded-lg border border-white/10 px-4 py-2 text-sm hover:border-white/20 transition-colors">
        Share
      </button>
      <button class="rounded-lg border border-accent-red/50 px-4 py-2 text-sm text-accent-red hover:bg-accent-red/10 transition-colors">
        Clear
      </button>
    </div>
  </div>
  
  <!-- Compatibility Banner -->
  <div class="mt-6 rounded-xl border {
    compatibility.status === 'ok' ? 'border-accent-green/30 bg-accent-green/5' :
    compatibility.status === 'warning' ? 'border-accent-amber/30 bg-accent-amber/5' :
    'border-accent-red/30 bg-accent-red/5'
  } p-4">
    <div class="flex items-center gap-3">
      <span class="text-xl">
        {compatibility.status === 'ok' ? '✅' : compatibility.status === 'warning' ? '⚠️' : '❌'}
      </span>
      <div class="flex-1">
        <p class="font-medium">{compatibility.message}</p>
        {#if compatibility.wattage}
          <p class="mt-1 text-sm text-text-secondary">
            ⚡ Estimated wattage: {compatibility.wattage.used}W 
            (PSU: {compatibility.wattage.available}W) 
            {compatibility.wattage.used < compatibility.wattage.available ? '✓' : '⚠️'}
          </p>
        {/if}
      </div>
    </div>
  </div>
  
  <!-- Component List -->
  <div class="mt-8 overflow-hidden rounded-xl border border-white/10">
    <table class="w-full">
      <thead>
        <tr class="border-b border-white/10 bg-bg-secondary text-left text-sm text-text-secondary">
          <th class="px-4 py-3 font-medium">Component</th>
          <th class="px-4 py-3 font-medium">Selection</th>
          <th class="px-4 py-3 font-medium text-right">Price</th>
        </tr>
      </thead>
      <tbody>
        {#each componentSlots as slot}
          <tr class="border-b border-white/5 last:border-0 hover:bg-bg-secondary/50 transition-colors">
            <td class="px-4 py-4">
              <div class="flex items-center gap-3">
                <span class="text-xl">{slot.icon}</span>
                <span class="font-medium">{slot.type}</span>
                {#if slot.required}
                  <span class="text-xs text-accent-red">*</span>
                {/if}
              </div>
            </td>
            <td class="px-4 py-4">
              {#if slot.selection}
                <div class="flex items-center gap-3">
                  <span class="text-text-primary">{slot.selection.name}</span>
                  <button class="text-sm text-text-tertiary hover:text-accent-blue transition-colors">
                    [Change]
                  </button>
                </div>
              {:else}
                <button class="flex items-center gap-2 text-accent-green hover:underline">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  Select {slot.type.toLowerCase()}
                </button>
                {#if slot.hint}
                  <p class="mt-1 text-xs text-text-tertiary">({slot.hint})</p>
                {/if}
              {/if}
            </td>
            <td class="px-4 py-4 text-right">
              {#if slot.selection}
                <span class="price font-medium">${slot.selection.price}</span>
              {:else}
                <span class="text-text-tertiary">—</span>
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
      <tfoot>
        <tr class="border-t-2 border-white/10 bg-bg-secondary">
          <td colspan="2" class="px-4 py-4 text-right font-semibold">
            Total
          </td>
          <td class="px-4 py-4 text-right">
            <span class="price text-xl font-bold text-accent-green">${totalPrice}</span>
          </td>
        </tr>
      </tfoot>
    </table>
  </div>
  
  <!-- Actions -->
  <div class="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <p class="text-sm text-text-secondary">
      💡 Cheapest combo: <span class="font-medium text-accent-green">$987</span> (mixed retailers)
    </p>
    
    <button class="flex items-center justify-center gap-2 rounded-lg bg-accent-green px-6 py-3 font-medium text-black hover:bg-accent-green/90 transition-colors">
      Buy All at Amazon
      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
      </svg>
    </button>
  </div>
  
  <!-- Tips -->
  <div class="mt-12 rounded-xl border border-white/10 bg-bg-secondary p-6">
    <h3 class="font-medium">💡 Build Tips</h3>
    <ul class="mt-3 space-y-2 text-sm text-text-secondary">
      <li>• The Ryzen 7 7800X3D is the best gaming CPU — excellent choice!</li>
      <li>• Your RTX 4070 will be limited by motherboard PCIe lanes — consider X670</li>
      <li>• 750W PSU recommended for this build with headroom</li>
    </ul>
  </div>
</div>
