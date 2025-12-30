<template>
  <AppLayout>
    <!-- KPI Cards -->
    <div class="grid grid-cols-2 gap-4 mb-6">
      <div class="card bg-success text-success-content">
        <div class="card-body p-4">
          <div class="text-xs opacity-80">Income</div>
          <div class="text-xl font-bold">{{ summary.income }}</div>
        </div>
      </div>

      <div class="card bg-error text-error-content">
        <div class="card-body p-4">
          <div class="text-xs opacity-80">Expenses</div>
          <div class="text-xl font-bold">{{ summary.expense }}</div>
        </div>
      </div>

      <div class="card bg-base-100 col-span-2">
        <div class="card-body p-4">
          <div class="text-xs opacity-70">Net Balance</div>
          <div
            class="text-2xl font-bold"
            :class="summary.net >= 0 ? 'text-success' : 'text-error'"
          >
            {{ summary.net }}
          </div>
        </div>
      </div>
    </div>

    <!-- Category Pie -->
    <div class="card bg-base-100 mb-6">
      <div class="card-body">
        <h2 class="font-semibold mb-3">Spending by Category</h2>
        <CategoryPie :categories="summary.by_category || []" />
      </div>
    </div>

    <!-- Filters -->
    <div class="flex gap-2 mb-3">
      <button
        v-for="f in filters"
        :key="f"
        class="btn btn-xs"
        :class="type === f ? 'btn-primary' : 'btn-outline'"
        @click="applyFilter(f)"
      >
        {{ f }}
      </button>
    </div>

    <!-- Transactions (Infinite Scroll Ready) -->
    <div class="card bg-base-100">
      <div class="card-body">
        <h2 class="font-semibold mb-2">Recent Transactions</h2>

        <div
          v-for="t in transactions"
          :key="t.id"
          class="flex justify-between border-b py-2 text-sm"
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

        <button
          class="btn btn-sm btn-outline mt-4 w-full"
          @click="loadMore"
        >
          Load more
        </button>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import CategoryPie from "@/components/CategoryPie.vue"
import api from "@/services/api"

const summary = ref({})
const transactions = ref([])
const page = ref(1)
const limit = 10
const type = ref(null)

const filters = ["All", "income", "expense", "transfer"]

const loadData = async (reset = false) => {
  if (reset) {
    transactions.value = []
    page.value = 1
  }

  const res = await api.get("/finance/transactions", {
    params: {
      page: page.value,
      limit,
      type: type.value === "All" ? null : type.value,
    },
  })

  transactions.value.push(...res.data.transactions)
  page.value++
}

const applyFilter = (f) => {
  type.value = f
  loadData(true)
}

const loadMore = () => loadData()

onMounted(async () => {
  const s = await api.get("/finance/summary")
  summary.value = s.data
  loadData()
})
</script>
