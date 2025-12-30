import BottomNav from "@/components/BottomNav.vue"


<template>
  <div class="min-h-screen bg-base-200 flex flex-col">
    <!-- Header -->
    <header class="navbar bg-base-100 shadow-sm">
      <div class="flex-1 text-lg font-bold px-2">
        MyJournal
      </div>
    </header>

    <!-- Page Content -->
    <main class="flex-1 p-4 pb-20">
      <slot />
    </main>

    <!-- Bottom Navigation -->
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue"
</script>
