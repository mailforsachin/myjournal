<template>
  <!-- Bottom Navigation - Mobile only -->
  <div class="btm-nav bg-base-100/95 backdrop-blur-sm border-t border-base-300 z-40 md:hidden">
    <!-- Dashboard -->
    <button
      @click="navigateTo('/dashboard')"
      class="flex flex-col items-center justify-center"
      :class="{ 'active': isActive('/dashboard') }"
    >
      <div class="text-2xl mb-1">📊</div>
      <span class="text-xs font-medium">Dashboard</span>
    </button>

    <!-- Finance -->
    <button
      @click="navigateTo('/transactions')"
      class="flex flex-col items-center justify-center"
      :class="{ 'active': isActive('/transactions') }"
    >
      <div class="text-2xl mb-1">💰</div>
      <span class="text-xs font-medium">Finance</span>
    </button>

    <!-- Language -->
    <button
      @click="navigateTo('/language')"
      class="flex flex-col items-center justify-center"
      :class="{ 'active': isActive('/language') }"
    >
      <div class="text-2xl mb-1">🌐</div>
      <span class="text-xs font-medium">Language</span>
    </button>

    <!-- PMP -->
    <button
      @click="navigateTo('/pmp')"
      class="flex flex-col items-center justify-center"
      :class="{ 'active': isActive('/pmp') }"
    >
      <div class="text-2xl mb-1">📚</div>
      <span class="text-xs font-medium">PMP</span>
    </button>

    <!-- Quotes -->
    <button
      @click="navigateTo('/quotes')"
      class="flex flex-col items-center justify-center"
      :class="{ 'active': isActive('/quotes') }"
    >
      <div class="text-2xl mb-1">💬</div>
      <span class="text-xs font-medium">Quotes</span>
    </button>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navigateTo = (path) => {
  router.push(path)
}

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}
</script>

<style scoped>
/* Fix DaisyUI btm-nav to be horizontal */
.btm-nav {
  display: flex !important;
  flex-direction: row !important;
  justify-content: space-around !important;
  height: 5rem !important;
}

.btm-nav > button {
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  min-width: 0 !important;
  padding: 0.5rem 0 !important;
}

.btm-nav > button.active {
  background-color: rgba(var(--color-primary) / 0.1) !important;
  border-top: 2px solid rgb(var(--color-primary)) !important;
}

/* Hide on desktop */
@media (min-width: 768px) {
  .btm-nav {
    display: none !important;
  }
}
</style>
