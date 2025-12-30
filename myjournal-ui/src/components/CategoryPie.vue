<template>
  <div class="h-64">
    <Pie :data="chartData" :options="options" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { Pie } from "vue-chartjs"
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js"

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  categories: {
    type: Array,
    required: true,
  },
})

const chartData = computed(() => ({
  labels: props.categories.map(c => c.category || "Uncategorized"),
  datasets: [
    {
      data: props.categories.map(c => Math.abs(c.total)),
      backgroundColor: [
        "#22c55e",
        "#ef4444",
        "#3b82f6",
        "#a855f7",
        "#f59e0b",
        "#14b8a6",
        "#e11d48",
      ],
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
}
</script>
