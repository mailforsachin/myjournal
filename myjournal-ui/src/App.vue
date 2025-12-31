<template>
  <div id="app">
    <!-- Show layout with navigation for authenticated routes -->
    <AppLayout 
      v-if="auth.isAuthenticated && !hideNavigation" 
      :title="currentTitle"
      :showBack="showBackButton"
    >
      <router-view />
    </AppLayout>
    
    <!-- Show only router view for login and non-authenticated pages -->
    <router-view v-else />
  </div>
</template>

<script setup>
import { computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

// Check authentication on app load
onMounted(() => {
  // Initialize auth - this will check if token exists and is valid
  auth.initialize?.()
})

// Computed properties
const hideNavigation = computed(() => {
  return route.meta.hideNavigation || false
})

const currentTitle = computed(() => {
  return route.meta.title || 'MyJournal'
})

const showBackButton = computed(() => {
  return route.meta.showBack !== false && route.path !== '/dashboard'
})

// Watch for authentication changes
watch(
  () => auth.isAuthenticated,
  (isAuthenticated) => {
    if (!isAuthenticated && route.meta.requiresAuth) {
      router.push('/login')
    }
    if (isAuthenticated && route.path === '/login') {
      router.push('/dashboard')
    }
  }
)

// Watch route changes
watch(
  () => route.path,
  (newPath) => {
    // Update document title
    document.title = route.meta.title 
      ? `${route.meta.title} - MyJournal` 
      : 'MyJournal'
  },
  { immediate: true }
)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

#app {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Smooth transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(var(--color-base-200) / 0.5);
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--color-base-content) / 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--color-base-content) / 0.5);
}
</style>
