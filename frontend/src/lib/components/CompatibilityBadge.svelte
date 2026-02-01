<script lang="ts">
  interface Props {
    status: 'compatible' | 'warning' | 'incompatible';
    message?: string;
  }
  
  let { status, message }: Props = $props();
  
  const icons = {
    compatible: '✅',
    warning: '⚠️',
    incompatible: '❌'
  };
  
  const colors = {
    compatible: 'text-accent-green bg-accent-green/10 border-accent-green/30',
    warning: 'text-accent-amber bg-accent-amber/10 border-accent-amber/30',
    incompatible: 'text-accent-red bg-accent-red/10 border-accent-red/30'
  };
  
  const labels = {
    compatible: 'Compatible',
    warning: 'Check compatibility',
    incompatible: 'Incompatible'
  };
</script>

<span class="inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-sm font-medium {colors[status]}">
  <span>{icons[status]}</span>
  <span>{message || labels[status]}</span>
</span>
