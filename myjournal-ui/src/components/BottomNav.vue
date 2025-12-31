<template>
  <div class="btm-nav fixed bottom-0 bg-base-100/95 backdrop-blur-lg border-t border-base-300 shadow-lg z-40 md:hidden">
    <RouterLink 
      to="/dashboard" 
      class="text-primary transition-all duration-300 flex flex-col items-center"
      :class="{ 'active': $route.path === '/dashboard' }"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      <span class="btm-nav-label text-xs font-medium">Dashboard</span>
    </RouterLink>

    <RouterLink 
      to="/transactions" 
      class="text-primary transition-all duration-300 flex flex-col items-center"
      :class="{ 'active': $route.path === '/transactions' }"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
      <span class="btm-nav-label text-xs font-medium">Transactions</span>
    </RouterLink>

    <RouterLink 
      to="/upload" 
      class="text-primary transition-all duration-300 flex flex-col items-center"
      :class="{ 'active': $route.path === '/upload' }"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      <span class="btm-nav-label text-xs font-medium">Upload</span>
    </RouterLink>

    <RouterLink 
      to="/rules" 
      class="text-primary transition-all duration-300 flex flex-col items-center"
      :class="{ 'active': $route.path === '/rules' }"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
      <span class="btm-nav-label text-xs font-medium">Rules</span>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.btm-nav a.active {
  @apply text-primary border-t-2 border-primary bg-primary/5;
}

.btm-nav a.active svg {
  @apply scale-110;
}
</style>
