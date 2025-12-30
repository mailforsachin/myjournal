import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {
    path: "/",
    component: { template: "<div>MyJournal UI Router OK</div>" },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
