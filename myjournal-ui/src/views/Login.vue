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
