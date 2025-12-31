<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-bold mb-2">Upload Transactions</h1>
      <p class="text-gray-600">Upload CSV files from your bank or credit card statements</p>
    </div>

    <!-- Upload Card -->
    <div class="card bg-base-100 shadow-lg border-2 border-dashed border-base-300 hover:border-primary transition-all">
      <div class="card-body">
        <!-- Upload Area -->
        <div 
          class="text-center py-12"
          @dragover.prevent="dragOver = true"
          @dragleave="dragOver = false"
          @drop.prevent="handleDrop"
          :class="{ 'bg-primary/5 border-primary': dragOver }"
        >
          <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center">
            <span class="text-3xl">📁</span>
          </div>
          
          <h3 class="text-lg font-semibold mb-2">Drop your CSV file here</h3>
          <p class="text-gray-500 mb-4">or click to browse</p>
          
          <input
            type="file"
            ref="fileInput"
            @change="handleFileSelect"
            accept=".csv,.txt"
            class="hidden"
          />
          
          <button
            @click="$refs.fileInput.click()"
            class="btn btn-primary"
            :disabled="uploading"
          >
            <span v-if="!uploading">Choose File</span>
            <span v-else class="flex items-center gap-2">
              <span class="loading loading-spinner loading-sm"></span>
              Uploading...
            </span>
          </button>
          
          <div v-if="selectedFile" class="mt-4">
            <div class="flex items-center justify-between bg-base-200 rounded-lg p-3">
              <div class="flex items-center gap-3">
                <span class="text-2xl">📄</span>
                <div>
                  <div class="font-medium">{{ selectedFile.name }}</div>
                  <div class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</div>
                </div>
              </div>
              <button @click="removeFile" class="btn btn-ghost btn-sm">
                ✕
              </button>
            </div>
            
            <button
              @click="uploadFile"
              class="btn btn-success btn-block mt-4"
              :disabled="!selectedFile || uploading"
            >
              <span v-if="!uploading">📤 Upload & Process</span>
              <span v-else class="flex items-center gap-2">
                <span class="loading loading-spinner loading-sm"></span>
                Processing...
              </span>
            </button>
          </div>
        </div>

        <!-- Sample Format -->
        <div class="mt-6 pt-6 border-t border-base-300">
          <h4 class="font-semibold mb-3">CSV Format Example:</h4>
          <div class="bg-base-200 rounded-lg p-4 overflow-x-auto">
            <pre class="text-sm">Date,Description,Amount,Category
2024-01-15,GROCERY STORE,-85.50,Groceries
2024-01-16,SALARY DEPOSIT,2500.00,Income
2024-01-17,AMAZON PURCHASE,-49.99,Shopping</pre>
          </div>
          <p class="text-sm text-gray-500 mt-2">
            Your CSV should have at least <strong>Date</strong> and <strong>Amount</strong> columns.
            Description and Category are optional.
          </p>
        </div>
      </div>
    </div>

    <!-- Results -->
    <div v-if="result" class="mt-6">
      <div class="card" :class="result.success ? 'bg-success/10 border-success' : 'bg-error/10 border-error'">
        <div class="card-body">
          <div class="flex items-center gap-3">
            <span class="text-2xl">{{ result.success ? '✅' : '❌' }}</span>
            <div>
              <h3 class="font-bold">{{ result.success ? 'Upload Successful!' : 'Upload Failed' }}</h3>
              <p class="mt-1">{{ result.message }}</p>
              <div v-if="result.stats" class="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3">
                <div class="stat bg-base-100 rounded-lg p-3">
                  <div class="stat-title">Total</div>
                  <div class="stat-value text-lg">{{ result.stats.total }}</div>
                </div>
                <div class="stat bg-base-100 rounded-lg p-3">
                  <div class="stat-title">Imported</div>
                  <div class="stat-value text-lg text-success">{{ result.stats.imported }}</div>
                </div>
                <div class="stat bg-base-100 rounded-lg p-3">
                  <div class="stat-title">Duplicates</div>
                  <div class="stat-value text-lg text-warning">{{ result.stats.duplicates }}</div>
                </div>
                <div class="stat bg-base-100 rounded-lg p-3">
                  <div class="stat-title">Failed</div>
                  <div class="stat-value text-lg text-error">{{ result.stats.failed }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="result.success" class="mt-4">
            <button @click="viewTransactions" class="btn btn-primary btn-sm">
              View Transactions →
            </button>
            <button @click="reset" class="btn btn-ghost btn-sm ml-2">
              Upload Another
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api' // Adjust path as needed

const router = useRouter()
const fileInput = ref(null)
const selectedFile = ref(null)
const uploading = ref(false)
const dragOver = ref(false)
const result = ref(null)

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && (file.name.endsWith('.csv') || file.name.endsWith('.txt'))) {
    selectedFile.value = file
  } else {
    alert('Please select a CSV file')
  }
}

const handleDrop = (event) => {
  dragOver.value = false
  const file = event.dataTransfer.files[0]
  if (file && (file.name.endsWith('.csv') || file.name.endsWith('.txt'))) {
    selectedFile.value = file
  } else {
    alert('Please drop a CSV file')
  }
}

const removeFile = () => {
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  result.value = null
  
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  
  try {
    // FIXED: Using correct endpoint /api/finance/upload-csv
    const response = await api.post('/finance/upload-csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    result.value = {
      success: true,
      message: response.data.message || 'File uploaded successfully',
      stats: response.data.stats || { total: 0, imported: 0, duplicates: 0, failed: 0 }
    }
    
  } catch (error) {
    console.error('Upload error:', error)
    result.value = {
      success: false,
      message: error.response?.data?.detail || error.message || 'Upload failed'
    }
  } finally {
    uploading.value = false
  }
}

const viewTransactions = () => {
  router.push('/transactions')
}

const reset = () => {
  selectedFile.value = null
  result.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
