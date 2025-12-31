<template>
  <!-- Filters -->
  <div class="flex gap-2 mb-4">
    <button
      v-for="t in filters"
      :key="t.value"
      class="btn btn-xs"
      :class="activeType === t.value ? 'btn-primary' : 'btn-outline'"
      @click="applyFilter(t.value)"
    >
      {{ t.label }}
    </button>
  </div>

  <!-- List -->
  <div class="card bg-base-100">
    <div class="card-body p-0">
      <div
        v-for="txn in transactions"
        :key="txn.id"
        class="flex justify-between p-4 border-b"
      >
        <div>
          <div class="font-medium text-sm">{{ txn.description }}</div>
          <div class="text-xs opacity-60">
            {{ txn.manual_category || txn.auto_category || "Uncategorized" }}
          </div>
        </div>

        <div class="text-right">
          <div
            class="font-semibold"
            :class="txn.amount < 0 ? 'text-error' : 'text-success'"
          >
            {{ txn.amount }}
          </div>

          <input
            type="checkbox"
            class="checkbox checkbox-xs"
            v-model="txn.confirmed"
            @change="toggleConfirm(txn)"
          />
        </div>
      </div>
    </div>
  </div>

  <button
    v-if="hasMore"
    class="btn btn-outline btn-sm w-full mt-4"
    @click="loadMore"
  >
    Load more
  </button>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "@/services/api"

const transactions = ref([])
const page = ref(1)
const hasMore = ref(true)
const activeType = ref(null)

const filters = [
  { label: "All", value: null },
  { label: "Expense", value: "expense" },
  { label: "Income", value: "income" },
  { label: "Transfer", value: "transfer" },
]

async function fetchTransactions(reset = false) {
  if (reset) {
    page.value = 1
    transactions.value = []
    hasMore.value = true
  }

  const params = { page: page.value, limit: 10 }
  if (activeType.value) params.type = activeType.value

  const res = await api.get("/finance/transactions", { params })

  if (res.data.transactions.length === 0) {
    hasMore.value = false
  } else {
    transactions.value.push(...res.data.transactions)
    page.value++
  }
}

function applyFilter(type) {
  activeType.value = type
  fetchTransactions(true)
}

async function toggleConfirm(txn) {
  await api.patch(`/finance/transactions/${txn.id}/category`, {
    manual_category: txn.manual_category,
    confirmed: txn.confirmed,
  })
}

function loadMore() {
  fetchTransactions()
}

onMounted(fetchTransactions)
</script>
