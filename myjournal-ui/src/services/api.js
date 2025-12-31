import axios from 'axios'
import { useAuthStore } from '../stores/auth'

// Axios instance
const api = axios.create({
  baseURL: '/api',          // Nginx will proxy this
  timeout: 15000,
  withCredentials: false,
})

// REQUEST interceptor
api.interceptors.request.use(
  (config) => {
    try {
      const auth = useAuthStore()
      if (auth?.token) {
        config.headers.Authorization = `Bearer ${auth.token}`
      }
    } catch (e) {
      // Pinia not ready yet (initial load) — safe to ignore
    }
    return config
  },
  (error) => Promise.reject(error)
)

// RESPONSE interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Network / backend down
    if (!error.response) {
      console.error('[API] Network error:', error.message)
      return Promise.reject(error)
    }

    // Unauthorized → logout once
    if (error.response.status === 401) {
      try {
        const auth = useAuthStore()
        auth.logout()
      } catch (e) {}

      if (!window.location.pathname.startsWith('/login')) {
        window.location.replace('/login')
      }
    }

    return Promise.reject(error)
  }
)

export default api
