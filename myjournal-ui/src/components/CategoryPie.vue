<template>
  <div class="h-64">
    <div v-if="loading" class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="loading loading-spinner loading-lg text-primary"></div>
        <p class="mt-2 text-sm text-base-content/70">Loading chart...</p>
      </div>
    </div>
    
    <div v-else-if="error" class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="text-4xl mb-2">❌</div>
        <p class="text-error">{{ error }}</p>
      </div>
    </div>
    
    <div v-else-if="!chartData" class="flex items-center justify-center h-full">
      <div class="text-center">
        <div class="text-4xl mb-2">📊</div>
        <p class="text-base-content/70">No category data available</p>
        <p class="text-xs text-base-content/50 mt-1">Upload some transactions first</p>
      </div>
    </div>
    
    <div v-else class="h-64">
      <Pie :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  }
})

const loading = ref(false)
const error = ref(null)
const chartData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        boxWidth: 12,
        padding: 15
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.label || '';
          if (label) {
            label += ': ';
          }
          label += '$' + Math.abs(context.raw).toLocaleString();
          return label;
        }
      }
    }
  }
}

const prepareChartData = (categories) => {
  if (!categories || categories.length === 0) {
    chartData.value = null
    return
  }

  // Filter out null categories and sort by absolute value
  const filtered = categories
    .filter(c => c.category && Math.abs(c.total) > 0)
    .sort((a, b) => Math.abs(b.total) - Math.abs(a.total))
    .slice(0, 8) // Top 8 categories

  if (filtered.length === 0) {
    chartData.value = null
    return
  }

  // Color palette
  const colors = [
    '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
    '#06b6d4', '#ec4899', '#84cc16', '#f97316', '#64748b'
  ]

  chartData.value = {
    labels: filtered.map(c => c.category),
    datasets: [{
      data: filtered.map(c => Math.abs(c.total)),
      backgroundColor: colors.slice(0, filtered.length),
      borderWidth: 1,
      borderColor: '#fff'
    }]
  }
}

watch(() => props.categories, (newCategories) => {
  loading.value = true
  error.value = null
  try {
    prepareChartData(newCategories)
  } catch (err) {
    error.value = 'Failed to prepare chart data'
    console.error('Chart error:', err)
  } finally {
    loading.value = false
  }
}, { immediate: true })
</script>
