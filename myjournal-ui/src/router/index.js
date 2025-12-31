import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "../stores/auth"

// Import views
import Login from "../views/Login.vue"
import Dashboard from "../views/Dashboard.vue"
import Upload from "../views/Upload.vue"
import Rules from "../views/Rules.vue"

// Lazy loading for better performance
const Transactions = () => import("../views/Transactions.vue")
const Language = () => import("../views/Language.vue")
const PMP = () => import("../views/PMP.vue")
const Quotes = () => import("../views/Quotes.vue")

const routes = [
  { 
    path: "/login", 
    component: Login,
    meta: { 
      hideNavigation: true,
      title: "Login"
    }
  },

  {
    path: "/dashboard",
    component: Dashboard,
    meta: { 
      requiresAuth: true,
      title: "Dashboard",
      showBack: false
    },
  },

  {
    path: "/transactions",
    component: Transactions,
    meta: { 
      requiresAuth: true,
      title: "Transactions",
      showBack: true
    },
  },

  {
    path: "/upload",
    component: Upload,
    meta: { 
      requiresAuth: true,
      title: "Upload CSV",
      showBack: true
    },
  },

  {
    path: "/rules",
    component: Rules,
    meta: { 
      requiresAuth: true,
      title: "Rules",
      showBack: true
    },
  },

  {
    path: "/language",
    component: Language,
    meta: { 
      requiresAuth: true,
      title: "Language Learning",
      showBack: true
    },
  },

  {
    path: "/pmp",
    component: PMP,
    meta: { 
      requiresAuth: true,
      title: "PMP Study",
      showBack: true
    },
  },

  {
    path: "/quotes",
    component: Quotes,
    meta: { 
      requiresAuth: true,
      title: "Daily Quotes",
      showBack: true
    },
  },

  // Default redirect to dashboard
  {
    path: "/",
    redirect: "/dashboard",
  },

  // 404 page redirect to dashboard
  {
    path: "/:pathMatch(.*)*",
    redirect: "/dashboard",
  },
]

// For production, use base URL if needed
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard with proper route handling
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  // Set document title
  document.title = to.meta.title 
    ? `${to.meta.title} - MyJournal` 
    : 'MyJournal'

  // Check if route requires authentication
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    // Store the attempted URL for redirect after login
    auth.redirectUrl = to.fullPath
    next("/login")
    return
  }

  // If already logged in and trying to access login page, redirect to dashboard
  if (to.path === "/login" && auth.isAuthenticated) {
    next("/dashboard")
    return
  }

  next()
})

export default router
