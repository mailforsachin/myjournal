<template>
  <div>
    <!-- Daily Quote -->
    <div class="card shadow-xl bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/20 mb-6">
      <div class="card-body">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="font-bold text-xl text-base-content">Quote of the Day</h2>
            <p class="text-sm text-base-content/70">{{ formatDate(new Date()) }}</p>
          </div>
          <div class="badge badge-primary badge-lg">Daily</div>
        </div>

        <blockquote class="text-2xl italic border-l-4 border-primary pl-4 py-2">
          "{{ dailyQuote.quote }}"
        </blockquote>

        <div class="mt-4 text-right">
          <p class="text-lg font-semibold">— {{ dailyQuote.author }}</p>
          <p class="text-sm text-base-content/70">{{ getCategoryLabel(dailyQuote.category) }}</p>
        </div>

        <div class="flex gap-2 mt-6">
          <button class="btn btn-ghost btn-sm" @click="saveQuote(dailyQuote)">Save</button>
          <button class="btn btn-ghost btn-sm" @click="shareQuote(dailyQuote)">Share</button>
          <button class="btn btn-ghost btn-sm ml-auto" @click="getRandomQuote">New Quote</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import quotesData from "@/data/quotes.csv?raw"

const quotes = ref([])
const dailyQuote = ref({})

const parseCSV = (csv) => {
  const lines = csv.split("\n")
  const headers = lines[0].split(",")
  const result = []

  for (let i = 1; i < lines.length && result.length < 10; i++) {
    if (!lines[i].trim()) continue
    const values = lines[i].split(",")
    const obj = {}
    headers.forEach((h, idx) => (obj[h.trim()] = values[idx]?.trim()))
    if (obj.quote && obj.author) result.push(obj)
  }
  return result
}

const loadQuotes = () => {
  quotes.value = parseCSV(quotesData)
  dailyQuote.value = quotes.value[0]
}

const getRandomQuote = () => {
  dailyQuote.value = quotes.value[Math.floor(Math.random() * quotes.value.length)]
}

const saveQuote = () => alert("Quote saved")
const shareQuote = () => alert("Quote copied")

const formatDate = (d) => new Date(d).toDateString()

const getCategoryLabel = (c) => c || "General"

onMounted(loadQuotes)
</script>
