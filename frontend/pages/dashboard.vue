<template>
  <div>
    <h1 class="text-3xl font-bold mb-4">Dashboard</h1>
    <button class="btn btn-primary" @click="load">Refresh Analytics</button>
    <div class="grid md:grid-cols-3 gap-4 mt-4">
      <div class="stat bg-base-200">
        <div class="stat-title">Events</div>
        <div class="stat-value">{{ stats.total || 0 }}</div>
      </div>
      <div class="card bg-base-200 p-4">
        <h3 class="font-semibold mb-2">By Type</h3>
        <div v-for="(v,k) in stats.by_type || {}" :key="k" class="flex justify-between py-1">
          <span>{{ k }}</span><span class="badge badge-outline">{{ v }}</span>
        </div>
      </div>
      <div class="card bg-base-200 p-4">
        <h3 class="font-semibold mb-2">Best Times</h3>
        <div v-for="(times,platform) in (stats.recommendations?.best_times || {})" :key="platform" class="mb-2">
          <div class="font-mono text-xs opacity-80">{{ platform }}</div>
          <div class="text-xs">{{ times.join(', ') }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const stats = ref({})
const { $api } = useNuxtApp() as any
async function load(){
  const { data } = await $api.get('/analytics/dashboard')
  stats.value = data
}
onMounted(load)
</script>
