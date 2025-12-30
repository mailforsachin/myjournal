import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "../stores/auth"
import Upload from "../views/Upload.vue"
import Login from "../views/Login.vue"
import Dashboard from "../views/Dashboard.vue"
import Rules from "../views/Rules.vue"

const routes = [
  {
    path: "/login",
    component: Login,
  },
  {
    path: "/dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/transactions",
    component: () => import("../views/Transactions.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/upload",
    component: Upload,
    meta: { requiresAuth: true },
  },
  {
    path: "/rules",
    component: Rules,
    meta: { requiresAuth: true },
  },
  {
    path: "/",
    redirect: "/dashboard",
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return "/login"
  }
})

export default router
