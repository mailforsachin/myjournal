<template>
  <div class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-end">
    <div class="bg-base-100 w-full rounded-t-xl p-4">
      <h3 class="font-bold">{{ txn.description }}</h3>

      <input
        class="input input-bordered w-full mt-3"
        v-model="category"
        placeholder="Manual category"
      />

      <label class="flex items-center gap-2 mt-3">
        <input type="checkbox" v-model="confirmed" class="checkbox" />
        Confirmed
      </label>

      <div class="flex gap-2 mt-4">
        <button class="btn btn-primary flex-1" @click="save">Save</button>
        <button class="btn btn-ghost flex-1" @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import api from "../api/axios"

const props = defineProps({ txn: Object })
const emit = defineEmits(["close", "updated"])

const category = ref(props.txn.manual_category || "")
const confirmed = ref(props.txn.confirmed === 1)

const save = async () => {
  await api.patch(`/api/finance/transactions/${props.txn.id}/category`, {
    manual_category: category.value,
    confirmed: confirmed.value,
  })

  emit("updated")
  emit("close")
}
</script>
