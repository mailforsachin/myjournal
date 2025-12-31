<template>
  <!-- Main Mobile Navigation -->
  <div class="fixed bottom-0 left-0 right-0 z-40 bg-base-100/95 backdrop-blur-lg border-t border-base-300 shadow-2xl">
    
    <!-- SECONDARY ROW - Finance Sub-navigation (only shows when on Finance routes) -->
    <div 
      v-if="isFinanceRoute" 
      class="flex justify-around items-center px-2 py-3 border-b border-base-300 bg-base-200/50"
    >
      <RouterLink
        to="/upload"
        class="flex flex-col items-center justify-center px-2"
        :class="{ 'text-primary': isActive('/upload') }"
      >
        <div class="w-12 h-12 rounded-full flex items-center justify-center mb-1"
          :class="isActive('/upload') ? 'bg-primary/20' : 'bg-base-300'">
          <span class="text-2xl">⬆️</span>
        </div>
        <span class="text-xs font-medium">Import</span>
      </RouterLink>

      <RouterLink
        to="/transactions"
        class="flex flex-col items-center justify-center px-2"
        :class="{ 'text-primary': isActive('/transactions') }"
      >
        <div class="w-12 h-12 rounded-full flex items-center justify-center mb-1"
          :class="isActive('/transactions') ? 'bg-primary/20' : 'bg-base-300'">
          <span class="text-2xl">📄</span>
        </div>
        <span class="text-xs font-medium">Transactions</span>
      </RouterLink>

      <RouterLink
        to="/rules"
        class="flex flex-col items-center justify-center px-2"
        :class="{ 'text-primary': isActive('/rules') }"
      >
        <div class="w-12 h-12 rounded-full flex items-center justify-center mb-1"
          :class="isActive('/rules') ? 'bg-primary/20' : 'bg-base-300'">
          <span class="text-2xl">⚙️</span>
        </div>
        <span class="text-xs font-medium">Auto-Categorize</span>
      </RouterLink>
    </div>

    <!-- PRIMARY ROW - Main Navigation (always visible) -->
    <div class="flex justify-around items-center px-1 py-3">
      <!-- Dashboard -->
      <RouterLink
        to="/dashboard"
        class="flex flex-col items-center justify-center flex-1 px-1"
        :class="{ 'text-primary': isActive('/dashboard') }"
      >
        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-1"
          :class="isActive('/dashboard') ? 'bg-primary/20' : 'bg-base-300/50'">
          <span class="text-xl">📊</span>
        </div>
        <span class="text-xs">Dashboard</span>
      </RouterLink>

      <!-- Finance -->
      <RouterLink
        to="/transactions"
        class="flex flex-col items-center justify-center flex-1 px-1"
        :class="{ 
          'text-primary': isFinanceRoute,
          'opacity-60': !isFinanceRoute 
        }"
      >
        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-1"
          :class="isFinanceRoute ? 'bg-primary/20' : 'bg-base-300/30'">
          <span class="text-xl">💰</span>
        </div>
        <span class="text-xs">Finance</span>
      </RouterLink>

      <!-- Language -->
      <RouterLink
        to="/language"
        class="flex flex-col items-center justify-center flex-1 px-1"
        :class="{ 
          'text-primary': isActive('/language'),
          'opacity-60': !isActive('/language') 
        }"
      >
        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-1"
          :class="isActive('/language') ? 'bg-primary/20' : 'bg-base-300/30'">
          <span class="text-xl">🌐</span>
        </div>
        <span class="text-xs">Language</span>
      </RouterLink>

      <!-- PMP -->
      <RouterLink
        to="/pmp"
        class="flex flex-col items-center justify-center flex-1 px-1"
        :class="{ 
          'text-primary': isActive('/pmp'),
          'opacity-60': !isActive('/pmp') 
        }"
      >
        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-1"
          :class="isActive('/pmp') ? 'bg-primary/20' : 'bg-base-300/30'">
          <span class="text-xl">📚</span>
        </div>
        <span class="text-xs">PMP</span>
      </RouterLink>

      <!-- Quotes -->
      <RouterLink
        to="/quotes"
        class="flex flex-col items-center justify-center flex-1 px-1"
        :class="{ 
          'text-primary': isActive('/quotes'),
          'opacity-60': !isActive('/quotes') 
        }"
      >
        <div class="w-10 h-10 rounded-full flex items-center justify-center mb-1"
          :class="isActive('/quotes') ? 'bg-primary/20' : 'bg-base-300/30'">
          <span class="text-xl">💬</span>
        </div>
        <span class="text-xs">Quotes</span>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router"
import { computed } from "vue"  // Fixed: Import computed from vue, not vue-router

const route = useRoute()

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + "/")
}

const isFinanceRoute = computed(() => {
  const financeRoutes = ['/transactions', '/upload', '/rules', '/finance']
  return financeRoutes.some(routePath => 
    route.path === routePath || route.path.startsWith(routePath + "/")
  )
})
</script>

<style scoped>
/* Animation for sub-navigation */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
  max-height: 80px;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}

/* Active state styling */
.router-link-active {
  @apply text-primary;
}

/* Ensure content doesn't hide behind nav */
.main-content {
  padding-bottom: 5rem;
}
</style>
