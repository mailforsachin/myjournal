<template>
  <div class="space-y-4">
    <div
      class="border-2 border-dashed rounded-xl p-6 text-center"
      :class="dragging ? 'border-primary bg-base-200' : 'border-base-300'"
      @dragover.prevent="dragging = true"
      @dragleave.prevent="dragging = false"
      @drop.prevent="handleDrop"
    >
      <p class="text-sm mb-2">Drag & drop CSV here</p>
      <input type="file" accept=".csv" @change="handleFile" />
    </div>

    <button class="btn btn-primary w-full" :disabled="!file || uploading" @click="upload">
      {{ uploading ? "Uploading..." : "Upload CSV" }}
    </button>

    <div v-if="result" class="alert alert-success">
      Imported {{ result.inserted }} rows
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import api from "@/services/api"
import AppLayout from "@/layouts/AppLayout.vue"

const file = ref(null)
const dragging = ref(false)
const uploading = ref(false)
const result = ref(null)

const handleFile = (e) => (file.value = e.target.files[0])
const handleDrop = (e) => {
  dragging.value = false
  file.value = e.dataTransfer.files[0]
}

const upload = async () => {
  uploading.value = true
  const form = new FormData()
  form.append("file", file.value)
  const res = await api.post("/finance/upload-csv", form)
  result.value = res.data
  uploading.value = false
}
</script>
