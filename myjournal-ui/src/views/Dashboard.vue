<template>
  <!-- Dashboard content ONLY -->
  <div class="pb-20"> <!-- Add padding-bottom for mobile nav -->

    <div class="mb-6">
      <h1 class="text-2xl font-bold">Dashboard</h1>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="card bg-success text-success-content">
        <div class="card-body">
          <div class="text-sm">Income</div>
          <div class="text-2xl font-bold">{{ summary.income }}</div>
        </div>
      </div>

      <div class="card bg-error text-error-content">
        <div class="card-body">
          <div class="text-sm">Expenses</div>
          <div class="text-2xl font-bold">{{ summary.expense }}</div>
        </div>
      </div>

      <div class="card bg-base-100">
        <div class="card-body">
          <div class="text-sm">Net</div>
          <div
            class="text-2xl font-bold"
            :class="summary.net >= 0 ? 'text-success' : 'text-error'"
          >
            {{ summary.net }}
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="card bg-base-100">
      <div class="card-body">
        <h2 class="font-bold mb-2">Recent Transactions</h2>

        <div
          v-for="t in transactions"
          :key="t.id"
          class="flex justify-between py-2 border-b text-sm"
        >
          <div>
            <div class="font-medium">{{ t.description }}</div>
            <div class="opacity-60">
              {{ t.manual_category || t.auto_category || "Uncategorized" }}
            </div>
          </div>

          <div :class="t.amount < 0 ? 'text-error' : 'text-success'">
            {{ t.amount }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/services/api"

const summary = ref({ income: 0, expense: 0, net: 0 })
const transactions = ref([])

onMounted(async () => {
  const s = await api.get("/finance/summary")
  summary.value = s.data

  const t = await api.get("/finance/transactions?limit=5")
  transactions.value = t.data.transactions
})
</script>
