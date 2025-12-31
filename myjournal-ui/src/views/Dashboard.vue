<template>
  <AppLayout>
    <!-- Welcome Header -->
    <div class="mb-6 fade-in">
      <div class="flex items-center justify-between mb-2">
        <div>
          <h1 class="text-2xl font-bold text-base-content">Welcome back!</h1>
          <p class="text-base-content/70 text-sm">Here's your financial overview</p>
        </div>
        <div class="text-xs px-3 py-1 rounded-full bg-primary/10 text-primary font-medium">
          {{ new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) }}
        </div>
      </div>
    </div>

    <!-- KPI Cards - Enhanced -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 fade-in">
      <div class="card bg-gradient-to-br from-success/90 to-success shadow-lg card-hover">
        <div class="card-body p-5 text-white">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-sm opacity-90 font-medium">Income</div>
              <div class="text-2xl font-bold mt-1">{{ formatCurrency(summary.income) }}</div>
            </div>
            <div class="p-3 rounded-full bg-white/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="text-xs opacity-80 mt-2">↑ 12% from last month</div>
        </div>
      </div>

      <div class="card bg-gradient-to-br from-error/90 to-error shadow-lg card-hover">
        <div class="card-body p-5 text-white">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-sm opacity-90 font-medium">Expenses</div>
              <div class="text-2xl font-bold mt-1">{{ formatCurrency(summary.expense) }}</div>
            </div>
            <div class="p-3 rounded-full bg-white/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
          </div>
          <div class="text-xs opacity-80 mt-2">↓ 8% from last month</div>
        </div>
      </div>

      <div class="card bg-gradient-to-br from-base-100 to-base-200 shadow-lg border border-base-300 card-hover">
        <div class="card-body p-5">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-sm opacity-70 font-medium">Net Balance</div>
              <div 
                class="text-2xl font-bold mt-1"
                :class="summary.net >= 0 ? 'text-success' : 'text-error'"
              >
                {{ formatCurrency(summary.net) }}
              </div>
            </div>
            <div class="p-3 rounded-full" :class="summary.net >= 0 ? 'bg-success/20' : 'bg-error/20'">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="summary.net >= 0 ? 'text-success' : 'text-error'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <div class="text-xs opacity-60 mt-2" :class="summary.net >= 0 ? 'text-success' : 'text-error'">
            {{ summary.net >= 0 ? 'Positive cash flow' : 'Negative cash flow' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Category Pie -->
      <div class="card bg-base-100 shadow-lg border border-base-300 card-hover fade-in">
        <div class="card-body">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-bold text-base-content">Spending by Category</h2>
            <div class="dropdown dropdown-end">
              <div tabindex="0" role="button" class="btn btn-ghost btn-sm">This month ▼</div>
              <ul tabindex="0" class="dropdown-content menu menu-sm bg-base-100 rounded-box shadow-lg border border-base-300 mt-1 p-2 w-40">
                <li><a>This month</a></li>
                <li><a>Last month</a></li>
                <li><a>This quarter</a></li>
                <li><a>This year</a></li>
              </ul>
            </div>
          </div>
          <CategoryPie :categories="summary.by_category || []" />
          <div class="text-xs text-base-content/60 text-center mt-4">
            Click on legend to toggle categories
          </div>
        </div>
      </div>

      <!-- Filters & Stats -->
      <div class="space-y-6">
        <!-- Quick Filters -->
        <div class="card bg-base-100 shadow-lg border border-base-300 card-hover fade-in">
          <div class="card-body p-5">
            <h2 class="font-bold text-base-content mb-4">Quick Filters</h2>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="f in filters"
                :key="f"
                class="btn btn-sm transition-all duration-300"
                :class="type === f ? 'btn-primary shadow-md' : 'btn-outline hover:btn-primary'"
                @click="applyFilter(f)"
              >
                {{ f }}
                <span v-if="f === 'All'" class="ml-1 text-xs opacity-70">{{ transactions.length }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Recent Transactions Preview -->
        <div class="card bg-base-100 shadow-lg border border-base-300 card-hover fade-in">
          <div class="card-body p-5">
            <div class="flex items-center justify-between mb-4">
              <h2 class="font-bold text-base-content">Recent Transactions</h2>
              <RouterLink to="/transactions" class="text-primary text-sm font-medium hover:underline">
                View all →
              </RouterLink>
            </div>
            
            <div class="space-y-3">
              <div
                v-for="(t, index) in recentTransactions"
                :key="t.id"
                class="flex items-center justify-between p-3 rounded-lg hover:bg-base-200 transition-all duration-300"
                :class="index < 3 ? '' : 'hidden md:flex'"
              >
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center" 
                       :class="t.amount < 0 ? 'bg-error/10 text-error' : 'bg-success/10 text-success'">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <div>
                    <div class="font-medium text-sm">{{ t.description }}</div>
                    <div class="text-xs opacity-60">
                      {{ t.manual_category || t.auto_category || "Uncategorized" }}
                    </div>
                  </div>
                </div>
                
                <div class="text-right">
                  <div :class="t.amount < 0 ? 'text-error font-bold' : 'text-success font-bold'">
                    {{ formatCurrency(t.amount) }}
                  </div>
                  <div class="text-xs opacity-60">
                    {{ formatDate(t.date) }}
                  </div>
                </div>
              </div>
            </div>

            <button
              class="btn btn-outline btn-sm w-full mt-4 hover:btn-primary transition-all duration-300"
              @click="loadMore"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Load more transactions
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Action Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 fade-in">
      <RouterLink to="/upload" class="card bg-gradient-to-br from-info/10 to-info/5 border border-info/20 card-hover group">
        <div class="card-body p-5">
          <div class="flex items-center gap-3">
            <div class="p-3 rounded-full bg-info/20 group-hover:bg-info/30 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-info" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div>
              <h3 class="font-bold text-base-content">Upload CSV</h3>
              <p class="text-sm opacity-70">Import new transactions</p>
            </div>
          </div>
        </div>
      </RouterLink>

      <RouterLink to="/rules" class="card bg-gradient-to-br from-warning/10 to-warning/5 border border-warning/20 card-hover group">
        <div class="card-body p-5">
          <div class="flex items-center gap-3">
            <div class="p-3 rounded-full bg-warning/20 group-hover:bg-warning/30 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-warning" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-bold text-base-content">Manage Rules</h3>
              <p class="text-sm opacity-70">Auto-categorize transactions</p>
            </div>
          </div>
        </div>
      </RouterLink>

      <div class="card bg-gradient-to-br from-base-100 to-base-200 border border-base-300 card-hover">
        <div class="card-body p-5">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-bold text-base-content">Export Report</h3>
              <p class="text-sm opacity-70">Download monthly summary</p>
            </div>
            <button class="btn btn-outline btn-sm hover:btn-primary">
              Export PDF
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import CategoryPie from "@/components/CategoryPie.vue"
import api from "@/services/api"

const summary = ref({ income: 0, expense: 0, net: 0, by_category: [] })
const transactions = ref([])
const page = ref(1)
const limit = 10
const type = ref(null)

const filters = ["All", "Income", "Expense", "Transfer"]

// Get only recent transactions for preview
const recentTransactions = computed(() => transactions.value.slice(0, 5))

const formatCurrency = (amount) => {
  if (amount === undefined || amount === null) return '$0.00'
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  })
  return formatter.format(amount)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

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
  try {
    const [summaryRes, transactionsRes] = await Promise.all([
      api.get("/finance/summary"),
      api.get("/finance/transactions", { params: { page: 1, limit } })
    ])
    
    summary.value = summaryRes.data
    transactions.value = transactionsRes.data.transactions
    page.value = 2
  } catch (error) {
    console.error("Failed to load dashboard data:", error)
  }
})
</script>
