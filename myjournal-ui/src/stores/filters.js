import { defineStore } from "pinia"

export const useFiltersStore = defineStore("filters", {
  state: () => ({
    year: new Date().getFullYear(),
    month: ""
  })
})
