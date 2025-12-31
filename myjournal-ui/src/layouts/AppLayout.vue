<template>
  <div class="min-h-screen bg-gradient-to-br from-base-100 to-base-200 flex flex-col fade-in">
    <!-- TOP BAR - Simplified for Mobile -->
    <header class="sticky top-0 z-50 bg-base-100/95 backdrop-blur-sm shadow-md border-b border-base-300">
      <div class="flex items-center justify-between px-4 py-3">
        <!-- Back button -->
        <button
          v-if="showBack"
          class="btn btn-ghost btn-square btn-sm"
          @click="$router.back()"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- Title -->
        <h1 class="text-lg font-bold flex-1 text-center px-2 truncate">
          {{ title || "MyJournal" }}
        </h1>

        <!-- User menu for mobile -->
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-ghost btn-square btn-sm">
            <div class="w-7 rounded-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
          <ul tabindex="0" class="dropdown-content menu menu-sm bg-base-100 rounded-box shadow-xl border border-base-300 mt-2 p-2 w-48">
            <li><a class="hover:bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>Profile</a></li>
            <li><a class="hover:bg-primary/10"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>Settings</a></li>
            <li><hr class="my-1 border-base-300" /></li>
            <li><a @click="logout" class="text-error hover:bg-error/10"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>Logout</a></li>
          </ul>
        </div>
      </div>

      <!-- Optional: Show current module indicator -->
      <div v-if="isFinanceRoute" class="px-4 pb-2">
        <div class="text-xs font-medium text-primary flex items-center gap-1">
          <span>📊</span>
          <span>Finance Module Active</span>
        </div>
      </div>
    </header>

    <!-- MAIN CONTENT AREA -->
    <main class="flex-1 p-4 pb-32 md:pb-6 overflow-y-auto">
      <slot />
    </main>

    <!-- MOBILE BOTTOM NAVIGATION -->
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter, useRoute } from "vue-router"
import { computed } from "vue"  // Fixed: Import computed from vue

defineProps({
  title: { type: String, default: "" },
  showBack: { type: Boolean, default: false },
})

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const isFinanceRoute = computed(() => {
  const financeRoutes = ['/transactions', '/upload', '/rules']
  return financeRoutes.some(routePath => 
    route.path === routePath || route.path.startsWith(routePath + "/")
  )
})

const logout = () => {
  auth.logout()
  router.push("/login")
}
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* For desktop, we can add a sidebar */
@media (min-width: 768px) {
  .app-layout {
    display: grid;
    grid-template-columns: 16rem 1fr;
  }
  
  header {
    grid-column: 1 / -1;
  }
  
  main {
    padding-bottom: 1rem;
  }
  
  /* Hide bottom nav on desktop */
  .btm-nav {
    display: none;
  }
  
  /* Add sidebar */
  .app-layout::before {
    content: '';
    grid-row: 2;
    grid-column: 1;
    background: linear-gradient(to bottom, rgba(var(--color-base-100), 0.9), rgba(var(--color-base-100), 0.7));
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(var(--color-base-300), 0.5);
  }
}
</style>
