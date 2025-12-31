<template>
  <AppLayout title="Category Rules" :showBack="true">
    <div class="space-y-4">
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
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import api from "@/services/api"

const text = ref("")
const saved = ref(false)

onMounted(async () => {
  const res = await api.get("/finance/rules")
  text.value = JSON.stringify(res.data, null, 2)
})

const save = async () => {
  await api.put("/finance/rules", JSON.parse(text.value))
  saved.value = true
  setTimeout(() => (saved.value = false), 2000)
}
</script>
