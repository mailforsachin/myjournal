<template>
  <div class="space-y-3">
    <!-- Filters -->
    <div class="flex gap-2 overflow-x-auto">
      <button class="btn btn-xs" @click="setFilter(null)">All</button>
      <button class="btn btn-xs" @click="setFilter('expense')">Expense</button>
      <button class="btn btn-xs" @click="setFilter('income')">Income</button>
      <button class="btn btn-xs" @click="setFilter('transfer')">Transfer</button>
    </div>

    <!-- Transactions -->
    <div
      v-for="txn in transactions"
      :key="txn.id"
      class="card bg-base-100 shadow p-3"
      @click="select(txn)"
    >
      <div class="flex justify-between">
        <div>
          <p class="font-medium">{{ txn.description }}</p>
          <p class="text-xs text-gray-500">
            {{ txn.auto_category || txn.manual_category || "Uncategorized" }}
          </p>
        </div>
        <div :class="txn.amount < 0 ? 'text-error' : 'text-success'">
          {{ txn.amount }}
        </div>
      </div>
    </div>

    <button v-if="!done" class="btn btn-sm w-full" @click="loadMore">
      Load more
    </button>

    <TransactionDetail
      v-if="selected"
      :txn="selected"
      @close="selected=null"
      @updated="reload"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../api/axios"
import TransactionDetail from "./TransactionDetail.vue"

const transactions = ref([])
const page = ref(1)
const filterType = ref(null)
const done = ref(false)
const selected = ref(null)

const load = async () => {
  const res = await api.get("/api/finance/transactions", {
    params: {
      page: page.value,
      limit: 10,
      type: filterType.value,
    },
  })

  if (res.data.transactions.length === 0) {
    done.value = true
    return
  }

  transactions.value.push(...res.data.transactions)
}

const loadMore = async () => {
  page.value++
  await load()
}

const setFilter = async (type) => {
  filterType.value = type
  page.value = 1
  done.value = false
  transactions.value = []
  await load()
}

const select = (txn) => {
  selected.value = txn
}

const reload = async () => {
  page.value = 1
  done.value = false
  transactions.value = []
  await load()
}

onMounted(load)
</script>
