<template>
  <div class="p-4 space-y-4">
    <h1 class="text-xl font-bold">Category Rules</h1>

    <textarea
      class="textarea textarea-bordered w-full h-[60vh] font-mono text-xs"
      v-model="text"
    ></textarea>

    <button class="btn btn-primary w-full" @click="save">
      Save Rules
    </button>

    <div v-if="saved" class="alert alert-success">
      Rules updated successfully
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../api/axios"

const text = ref("")
const saved = ref(false)

onMounted(async () => {
  const res = await api.get("/api/finance/rules")
  text.value = JSON.stringify(res.data, null, 2)
})

const save = async () => {
  await api.put("/api/finance/rules", JSON.parse(text.value))
  saved.value = true
  setTimeout(() => (saved.value = false), 2000)
}
</script>
