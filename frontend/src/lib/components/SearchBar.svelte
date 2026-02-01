<script lang="ts">
  import { goto } from '$app/navigation';
  
  interface Props {
    value?: string;
    autofocus?: boolean;
    size?: 'default' | 'large';
  }
  
  let { value = $bindable(''), autofocus = false, size = 'default' }: Props = $props();
  
  function handleSubmit(e: Event) {
    e.preventDefault();
    if (value.trim()) {
      goto(`/search?q=${encodeURIComponent(value)}`);
    }
  }
</script>

<form onsubmit={handleSubmit} class="relative w-full">
  <input
    type="text"
    bind:value
    placeholder="Search parts... (RTX 4070, Ryzen 7, 32GB DDR5)"
    {autofocus}
    class="w-full rounded-xl border border-white/10 bg-bg-secondary placeholder-text-tertiary focus:border-accent-green focus:outline-none focus:ring-2 focus:ring-accent-green/20 transition-all
      {size === 'large' ? 'px-6 py-4 pl-14 text-lg' : 'px-4 py-3 pl-11 text-base'}"
  />
  <svg 
    class="absolute top-1/2 -translate-y-1/2 text-text-tertiary
      {size === 'large' ? 'left-5 h-5 w-5' : 'left-4 h-4 w-4'}" 
    fill="none" 
    stroke="currentColor" 
    viewBox="0 0 24 24"
  >
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
  </svg>
  <button 
    type="submit"
    class="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg bg-accent-green font-medium text-black hover:bg-accent-green/90 transition-colors
      {size === 'large' ? 'px-4 py-2' : 'px-3 py-1.5 text-sm'}"
  >
    Search
  </button>
</form>
