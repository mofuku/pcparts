<script lang="ts">
  import '../app.css';
  
  let { children } = $props();
</script>

<div class="min-h-screen bg-bg-primary text-text-primary">
  <!-- Navigation -->
  <nav class="sticky top-0 z-50 border-b border-white/10 bg-bg-primary/80 backdrop-blur-lg">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <!-- Logo -->
        <a href="/" class="flex items-center gap-2 text-xl font-bold text-text-primary hover:text-accent-green transition-colors">
          <svg class="h-8 w-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="8" width="24" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
            <rect x="8" y="12" width="6" height="8" fill="currentColor" opacity="0.5"/>
            <rect x="16" y="12" width="2" height="8" fill="currentColor"/>
            <rect x="20" y="12" width="2" height="8" fill="currentColor"/>
          </svg>
          PCParts
        </a>
        
        <!-- Desktop Nav -->
        <div class="hidden md:flex items-center gap-6">
          <a href="/search" class="text-text-secondary hover:text-text-primary transition-colors">
            Search
          </a>
          <a href="/build" class="text-text-secondary hover:text-text-primary transition-colors">
            Build
          </a>
          <a href="/deals" class="text-text-secondary hover:text-text-primary transition-colors">
            Deals
          </a>
        </div>
        
        <!-- CTA -->
        <div class="flex items-center gap-4">
          <a 
            href="/build" 
            class="hidden sm:flex items-center gap-2 rounded-lg bg-accent-green px-4 py-2 text-sm font-medium text-black hover:bg-accent-green/90 transition-colors"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Start Build
          </a>
        </div>
      </div>
    </div>
  </nav>
  
  <!-- Main Content -->
  <main>
    {@render children()}
  </main>
  
  <!-- Footer -->
  <footer class="border-t border-white/10 bg-bg-secondary mt-auto">
    <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-sm text-text-tertiary">
          © 2025 PCParts. Find parts, not ads.
        </p>
        <div class="flex gap-6 text-sm text-text-tertiary">
          <a href="/about" class="hover:text-text-secondary transition-colors">About</a>
          <a href="/privacy" class="hover:text-text-secondary transition-colors">Privacy</a>
          <a href="https://github.com" class="hover:text-text-secondary transition-colors">GitHub</a>
        </div>
      </div>
    </div>
  </footer>
</div>
