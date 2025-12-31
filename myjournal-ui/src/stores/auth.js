import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  
  // State
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const redirectUrl = ref('')

  // Computed
  const isAuthenticated = computed(() => !!token.value)
  const getAuthHeaders = computed(() => {
    return {
      'Authorization': `Bearer ${token.value}`
    }
  })

  // Actions
  const login = async (username, password) => {
    try {
      const response = await axios.post('/api/login', {
        username,
        password
      })

      if (response.data.access_token) {
        token.value = response.data.access_token
        user.value = { username }
        
        // Save to localStorage
        localStorage.setItem('token', token.value)
        localStorage.setItem('user', JSON.stringify(user.value))

        // Redirect to saved URL or dashboard
        const redirect = redirectUrl.value || '/dashboard'
        redirectUrl.value = ''
        router.push(redirect)
        
        return { success: true }
      }
    } catch (error) {
      console.error('Login failed:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const checkAuth = async () => {
    if (!token.value) return false

    try {
      // Verify token with backend
      await axios.get('/api/verify', {
        headers: { 'Authorization': `Bearer ${token.value}` }
      })
      return true
    } catch (error) {
      console.error('Token verification failed:', error)
      // Auto logout if token is invalid
      logout()
      return false
    }
  }

  const getCurrentUser = async () => {
    if (!token.value) return null
    
    try {
      const response = await axios.get('/api/me', {
        headers: { 'Authorization': `Bearer ${token.value}` }
      })
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
      return user.value
    } catch (error) {
      console.error('Failed to get user:', error)
      return user.value
    }
  }

  // Initialize on store creation
  const initialize = async () => {
    if (token.value) {
      await checkAuth()
    }
  }

  // Call initialize
  initialize()

  return {
    // State
    token,
    user,
    redirectUrl,
    
    // Computed
    isAuthenticated,
    getAuthHeaders,
    
    // Actions
    login,
    logout,
    checkAuth,
    getCurrentUser
  }
})
