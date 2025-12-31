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
