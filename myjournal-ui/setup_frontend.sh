#!/bin/bash

# setup_frontend.sh - Automatic Vue.js Frontend Setup Script

echo "🚀 Starting frontend project setup..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p src/{api,stores,router,views}

# 1️⃣ Create src/api/axios.js
echo "📄 Creating src/api/axios.js..."
cat > src/api/axios.js << 'EOF'
import axios from "axios"

const api = axios.create({
  baseURL: "https://myjournal.omchat.ovh",
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
EOF

# 2️⃣ Create src/stores/auth.js
echo "📄 Creating src/stores/auth.js..."
cat > src/stores/auth.js << 'EOF'
import { defineStore } from "pinia"
import api from "../api/axios"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null

      try {
        const res = await api.post("/api/login", {
          username,
          password,
        })

        this.token = res.data.access_token
        localStorage.setItem("token", this.token)
      } catch (err) {
        this.error = "Invalid credentials"
        throw err
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = null
      localStorage.removeItem("token")
    },
  },
})
EOF

# 3️⃣ Create src/router/index.js
echo "📄 Creating src/router/index.js..."
cat > src/router/index.js << 'EOF'
import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "../stores/auth"

import Login from "../views/Login.vue"
import Dashboard from "../views/Dashboard.vue"

const routes = [
  {
    path: "/login",
    component: Login,
  },
  {
    path: "/",
    component: Dashboard,
    meta: { requiresAuth: true },
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
EOF

# 4️⃣ Create src/views/Login.vue
echo "📄 Creating src/views/Login.vue..."
cat > src/views/Login.vue << 'EOF'
<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200 px-4">
    <div class="card w-full max-w-sm shadow-xl bg-base-100">
      <div class="card-body">
        <h2 class="text-center text-2xl font-bold">MyJournal</h2>

        <form @submit.prevent="submit">
          <div class="form-control">
            <label class="label">Username</label>
            <input
              v-model="username"
              type="text"
              class="input input-bordered"
              required
            />
          </div>

          <div class="form-control mt-3">
            <label class="label">Password</label>
            <input
              v-model="password"
              type="password"
              class="input input-bordered"
              required
            />
          </div>

          <p v-if="error" class="text-error text-sm mt-2">
            {{ error }}
          </p>

          <button
            class="btn btn-primary w-full mt-4"
            :class="{ loading }"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "../stores/auth"

const username = ref("")
const password = ref("")
const auth = useAuthStore()
const router = useRouter()

const loading = auth.loading
const error = auth.error

const submit = async () => {
  try {
    await auth.login(username.value, password.value)
    router.push("/")
  } catch (e) {}
}
</script>
EOF

# 5️⃣ Create src/views/Dashboard.vue
echo "📄 Creating src/views/Dashboard.vue..."
cat > src/views/Dashboard.vue << 'EOF'
<template>
  <div class="p-4">
    <h1 class="text-xl font-bold">Dashboard</h1>
    <p class="mt-2 text-gray-500">
      Backend connected. Next: charts & transactions.
    </p>

    <button class="btn btn-sm mt-4" @click="logout">
      Logout
    </button>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth"

const auth = useAuthStore()

const logout = () => {
  auth.logout()
  location.href = "/login"
}
</script>
EOF

# 6️⃣ Create src/App.vue
echo "📄 Creating src/App.vue..."
cat > src/App.vue << 'EOF'
<template>
  <router-view />
</template>
EOF

# 7️⃣ Create src/main.js
echo "📄 Creating src/main.js..."
cat > src/main.js << 'EOF'
import { createApp } from "vue"
import { createPinia } from "pinia"
import router from "./router/index"
import App from "./App.vue"
import "./style.css"

createApp(App)
  .use(createPinia())
  .use(router)
  .mount("#app")
EOF

# 8️⃣ Create src/style.css (basic Tailwind setup)
echo "📄 Creating src/style.css..."
cat > src/style.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# 9️⃣ Create package.json if not exists
if [ ! -f "package.json" ]; then
  echo "📄 Creating package.json..."
  cat > package.json << 'EOF'
{
  "name": "myjournal-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "pinia": "^2.1.7",
    "vue-router": "^4.2.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "vite": "^5.0.0"
  }
}
EOF
fi

# 🔟 Create vite.config.js if not exists
if [ ! -f "vite.config.js" ]; then
  echo "📄 Creating vite.config.js..."
  cat > vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
})
EOF
fi

# 1️⃣1️⃣ Create tailwind.config.js if not exists
if [ ! -f "tailwind.config.js" ]; then
  echo "📄 Creating tailwind.config.js..."
  cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF
fi

# 1️⃣2️⃣ Create postcss.config.js if not exists
if [ ! -f "postcss.config.js" ]; then
  echo "📄 Creating postcss.config.js..."
  cat > postcss.config.js << 'EOF'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF
fi

# 1️⃣3️⃣ Create index.html if not exists
if [ ! -f "index.html" ]; then
  echo "📄 Creating index.html..."
  cat > index.html << 'EOF'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@3.9.4/dist/full.css" rel="stylesheet" type="text/css" />
    <script src="https://cdn.tailwindcss.com"></script>
    <title>MyJournal</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
EOF
fi

# 1️⃣4️⃣ Verify structure
echo "📊 Verifying structure..."
find src -type f | sort

echo ""
echo "✅ Setup complete! Directory structure:"
tree src/ 2>/dev/null || find src/ -type f | sed -e "s/[^-][^\/]*\//  |/g" -e "s/|\([^ ]\)/|-\1/"

# 1️⃣5️⃣ Install dependencies and start dev server
echo ""
echo "📦 Installing dependencies..."
npm install

# 1️⃣6️⃣ Restart dev server
echo "🔄 Restarting development server..."
pkill -f vite 2>/dev/null || true
rm -rf node_modules/.vite 2>/dev/null || true

echo ""
echo "🚀 Starting development server..."
npm run dev -- --host &

echo ""
echo "✅ Setup complete! Your frontend is ready with:"
echo "   • JWT authentication with Axios interceptors"
echo "   • Pinia store for state management"
echo "   • Vue Router with protected routes"
echo "   • Mobile-first responsive design"
echo "   • DaisyUI + Tailwind CSS"
echo ""
echo "📱 Test the application at: http://localhost:5173"
echo "   Login page: http://localhost:5173/login"
echo ""
echo "⚡ To restart dev server manually: npm run dev -- --host"
