<template>
  <div class="p-4 space-y-4">
    <h1 class="text-xl font-bold">Upload Bank CSV</h1>

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

    <button
      class="btn btn-primary w-full"
      :disabled="!file || uploading"
      @click="upload"
    >
      {{ uploading ? "Uploading..." : "Upload CSV" }}
    </button>

    <div v-if="result" class="alert alert-success">
      Imported {{ result.inserted }} rows
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import api from "../api/axios"

const file = ref(null)
const dragging = ref(false)
const uploading = ref(false)
const result = ref(null)

const handleFile = (e) => {
  file.value = e.target.files[0]
}

const handleDrop = (e) => {
  dragging.value = false
  file.value = e.dataTransfer.files[0]
}

const upload = async () => {
  const form = new FormData()
  form.append("file", file.value)

  uploading.value = true
  const res = await api.post("/api/finance/upload-csv", form)
  uploading.value = false
  result.value = res.data
}
</script>
