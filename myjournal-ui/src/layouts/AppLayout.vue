<template>
  <div class="min-h-screen bg-base-200 flex flex-col">

    <!-- TOP BAR -->
    <header class="navbar bg-base-100 shadow-sm px-3">
      <div class="flex-1 flex items-center gap-2">
        <button
          v-if="showBack"
          class="btn btn-ghost btn-sm"
          @click="$router.back()"
        >
          ←
        </button>
        <span class="text-lg font-bold">{{ title || "MyJournal" }}</span>
      </div>

      <div class="flex-none">
        <button class="btn btn-ghost btn-sm" @click="logout">
          Logout
        </button>
      </div>
    </header>

    <!-- PAGE CONTENT -->
    <main class="flex-1 p-4 pb-20">
      <slot />
    </main>

    <!-- BOTTOM NAV -->
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

defineProps({
  title: { type: String, default: "" },
  showBack: { type: Boolean, default: false },
})

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push("/login")
}
</script>
